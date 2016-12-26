const doc = """
git-rsync - Export/import large files using rsync.

Usage:
  git-rsync init [<storage>]
  git-rsync push [<dir>]
  git-rsync pull [<dir>]
"""

import os
import osproc
import system
import strutils
import strfmt
import docopt
import future

# Exceptions of UserError type are considered as mistakes of the user. They should be displayed without traceback.
# Remaining Exceptions are considered as bugs in the application and should be displayed with traceback.
type
  UserError = object of Exception

const storageName = "storage"
const fileListName = ".gitrsync"

proc os_windows(): bool =
  # Detect operating system.
  return ExeExt == "exe"

proc gitPathToCygDrivePath(path: string): string =
  # Convert path used by git to the one which will be accepted by cwRsync.
  # under windows git uses paths of folowing format:
  # c:/foo/bar/baz
  # rsync expects:
  # /cygdrive/c/foo/bar/baz
  if os_windows() and len(path) >= 2 and path[1] == ':':
    return "/cygdrive/" & path[0] & path[2..^1]
  else:
    return path
    
proc firstLine(text: string): string =
  # Split test into lines and return the first one. \r \n will be stripped.
  return text.splitLines()[0]

proc shell(cmd: string, errorMsg: string) =
  # Executes command in underlying shell and raises exception if returned values is not 0
  var code: int
  echo cmd
  code = execCmd(cmd)
  if code != 0:
    raise newException(Exception, errorMsg)
  
proc getStorage(): tuple[path: string, isEmbedded: bool] =
  # Find location of storage directory  
  # 1. Try to find location in git config
  # 2. Try to find storage in remote repo
  # 3. Assume that storage exists in .git directory
  var outp: string
  var code: int

  (outp, code) = execCmdEx("git config --get rsync.url")
  if code == 0:
    return (gitPathToCygDrivePath(outp.firstLine), false)

  (outp, code) = execCmdEx("git config --get remote.origin.url")
  if code == 0:
    return (gitPathToCygDrivePath(outp.firstLine) & "/" & storageName & "/", false)

  return (".git/" & storageName & "/", true)

proc getTag(): string =
  # Find the most recent tag. Optionally filter out tags excluded in git config.
  var
    outp: string
    code: int
    match_opt: seq[string]

  (outp, code) = execCmdEx("git config --get rsync.tag")
  if code == 0:
    match_opt = @["--match", outp.firstLine]
  else:
    match_opt = @[]

  let cmd_seq = @["git describe --abbrev=0 --tags"] & match_opt

  (outp, code) = execCmdEx(cmd_seq.join(" "))
  if code == 0:
    return outp.firstLine
  else:
    raise newException(UserError, "Last tag cannot be determined")

proc getDir(dir_arg: Value): string =
  # Return dir_arg if it is specified by the user. Otherwise return the most recent tag.
  if dir_arg.kind == vkNone:
    return getTag()
  else:
    return $dir_arg
  
proc getUrl(dir_arg: Value): string =
  # Combine location of the storage with specifed directory.
  let
    (storage, _) = getStorage()
    dir = getDir(dir_arg)
  return "\"" & storage & dir & "/" & "\""

proc getRsyncProp(propName: string, default: string): string =
  # Read given property from git config.
  var outp: string
  var code: int

  (outp, code) = execCmdEx("git config --get rsync." & propName)
  if code == 0:
    return outp.firstLine
  else:
    return default

proc getSrc(): string =
  # Read list of files to be exported by rsync. Each file should be specified in separate
  # line of .gitrsync file. Patterns (e.g. specifed by sterisk) are also allowed, but keep
  # in mind that they are resolved by underlying shell. Names containing spaces must be
  # encapsulated in double quotes.
  let
    fh = open(fileListName, mode=fmRead)
    lines = fh.readAll().splitLines()
  fh.close()
  let
    nonEmpty = lc[t.strip() | (t <- lines, len(t)>0), string]
    notComment = lc[t | (t <- nonEmpty, t[0] != '#'), string]
    src = notComment.join(" ")
  return src
    
proc cmd_init(storage_arg: Value) =
  # Create storage directory (in local .git directory and in the remote one) and .gitrsync file.
  if storage_arg.kind != vkNone:
    let cmd = "git config --add rsync.url " & $storage_arg
    shell(cmd, "Cannot configure storage URL")

  let
    (storage, isEmbedded) = getStorage()
    fh = open(fileListName, mode=fmWrite)
    embeddedStoragePath = ".git/" & storageName & "/"

  fh.write("# List of the files to be exported by rsync.")
  fh.close()
  os.createDir(embeddedStoragePath)
  
  if not isEmbedded:
      let cmd = "rsync -rav " & embeddedStoragePath & " " & storage
      shell(cmd, "Error while creating storage")

proc cmd_push(dir_arg: Value) =
  # Copy files defined in .gitrsync to given directory in the storage.
  let
    tmpl = getRsyncProp("push", "rsync -Rrav --progress {src} {url}")
    url = getUrl(dir_arg)
    src = getSrc()
    cmd = tmpl.replace("{url}", url).replace("{src}", src)

  shell(cmd, "Error while pushing files to the storage")

proc cmd_pull(dir_arg: Value) =
  # Copy files from given directory in the storage to the local directory.
  let
    tmpl = getRsyncProp("pull", "rsync -rav --progress {url} .")
    url = getUrl(dir_arg)
    cmd = tmpl.replace("{url}", url)

  shell(cmd, "Error while pulling files from the storage")


when isMainModule:
  try:
    let args = docopt(doc)
    if args["init"]:
      cmd_init(args["<storage>"])
    elif args["push"]:
      cmd_push(args["<dir>"])
    elif args["pull"]:
      cmd_pull(args["<dir>"])

  except UserError:
    echo getCurrentExceptionMsg()

    
