#!/usr/bin/python

from genericpath import exists, isdir
import glob;
import subprocess;
import sys;
import os;

IDK="../build/nava"
FAILED=[]
PASSED=[]
NOT_REC=[]
NAVA_FILES=glob.glob("./**/*.nava", recursive=True)

def compile(path: str):
    subprocess.call([IDK, "-s", path, "-i", "../nava/System.nava", "-r", "./"])

def compile_and_run(path: str):
    compile(path)
    parts = path.split('/');
    s = "./main > " + '/'.join(parts[0:-1]) + '/' + parts[len(parts)-1].split(".")[0] + ".temp"
    subprocess.call(["sh", "-c", s])
    if exists('/'.join(parts[0:-1]) + '/' + parts[len(parts)-1].split(".")[0] + ".txt"):
        if open('/'.join(parts[0:-1]) + '/' + parts[len(parts)-1].split(".")[0] + ".temp", "r").read() != open('/'.join(parts[0:-1]) + '/' + parts[len(parts)-1].split(".")[0] + ".txt", "r").read():
            print("\u001b[31mFailed test:\u001b[0m %s" % path)
            print("Expected:")
            print(open('/'.join(parts[0:-1]) + '/' + parts[len(parts)-1].split(".")[0] + ".txt", "r").read())
            print("Got:")
            print(open('/'.join(parts[0:-1]) + '/' + parts[len(parts)-1].split(".")[0] + ".temp", "r").read())
            FAILED.append(path);
        else:
            print("\u001b[32mPassed test:\u001b[0m %s" % path)
            PASSED.append(path);
        os.remove('/'.join(parts[0:-1]) + '/' + parts[len(parts)-1].split(".")[0] + ".temp")
    else:
        NOT_REC.append(path)

def compile_run_all():
    nava_files = glob.glob("./**/*.nava", recursive=True)
    for nava in nava_files:
        if os.path.isdir(nava) :
            continue
        if nava == "./System.nava":
            continue
        else:
            compile_and_run(nava)

def compile_and_record(path: str):
    compile(path)
    parts = path.split('/');
    
    s = "./main > "

    if len(parts) == 1:
        s += parts[len(parts)-1].split(".")[0] + ".txt"
    else:
        s +=  '/'.join(parts[0:-1]) + '/' + parts[len(parts)-1].split(".")[0] + ".txt"
    subprocess.call(["sh", "-c", s])

def compile_record_all():
    for nava in NAVA_FILES:
        if os.path.isdir(nava) :
            continue
        if nava == "./System.nava":
            continue
        else:
            compile_and_record(nava)

if __name__ == "__main__":
    assert len(sys.argv) > 1, "Not enought arguments."
    if(sys.argv[1] == "-a"):
        compile_run_all()
        print()
        print("PASSED:       %02d/%02d" % (len(PASSED), len(NAVA_FILES)))
        print("FAILED:       %02d/%02d" % (len(FAILED), len(NAVA_FILES)))
        for fail in FAILED:
            print("\t%s" % fail)
        print("NOT RECORDED: %02d/%02d" % (len(NOT_REC), len(NAVA_FILES)))
        for no_rec in NOT_REC:
            print("\t%s" % no_rec)
        print()
    elif sys.argv[1] == "-ra":
        compile_record_all()
    elif sys.argv[1] == "-r":
        compile_and_record(sys.argv[2])
    else:
        compile_and_run(sys.argv[1])
    