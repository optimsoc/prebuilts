#!/usr/bin/python

from optparse import OptionParser
import subprocess, os, sys

if sys.version_info.major == 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

prebuilts = {
    "or1kelf": {
        "name": "or1k-elf-multicore",
        "tgz": "or1k-elf-multicore_gcc5.3.0_binutils2.26_newlib2.3.0-1_gdb7.11.tgz",
        "url": "https://github.com/openrisc/newlib/releases/download/v2.3.0-1/",
        "tar_extra": "--strip-components=1",
        "dest": "toolchains",
        "env": [
            { "var": "PATH",
              "type": "list-prepend",
              "value": "{base}/bin" }
        ]
    },
    "verilator": {
        "name": "verilator-3.882",
        "tgz": "verilator-3.882.tgz",
        "url": "https://raw.githubusercontent.com/optimsoc/prebuilts/master/",
        "dest": "prebuilt",
        "relocate": "relocate.sh",
        "env": [
            { "var": "VERILATOR_ROOT",
              "value": "{base}" },
            { "var": "PATH",
              "type": "list-prepend",
              "value": "{base}/bin" },
            { "var": "PKG_CONFIG_PATH",
              "type": "list-prepend",
              "value": "{base}/pkgconfig" }
        ]
    }
}

if __name__ == '__main__':
    usage = "usage: %prog [options] <prebuilt list>"
    epilog = "<prebuilt list> is either 'all' or a list of:"
    for p in prebuilts:
        epilog += " {}".format(p)

    parser = OptionParser(usage=usage, epilog=epilog)
    parser.add_option("-d", "--destination", dest="dest",
                      help="destination folder", default="/opt/optimsoc")

    (options, args) = parser.parse_args()

    if "all" not in args:
        for p in list(prebuilts):
            if p not in args:
                prebuilts.pop(p)

    if len(prebuilts) == 0:
        print("No prebuilts given.")
        parser.print_help()
        exit(0)

    setup_sh = [ "# Auto-generated, do not change" ]

    for key in prebuilts:
        print("Install {}".format(key))
        p = prebuilts[key]

        print(" + Download")
        tgz = p["tgz"]
        url = "{}/{}".format(p["url"], tgz)
        tmp = "/tmp/{}".format(tgz)
        urlretrieve(url, tmp)

        print(" + Extract")
        out = os.path.join(options.dest, p["dest"])

        try:
            os.makedirs(out)
        except OSError as e:
            if e.errno != 17:
                print("Cannot make output dir {}: {}", out, e)

        tar_extra = ""
        if "tar_extra" in p:
            tar_extra = p["tar_extra"]

        cmd = "tar -xzf {} {} -C {}".format(tmp, tar_extra, out)
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            print("tar error: {}\n{}".format(e, e.output))
            exit(1)

        if "relocate" in p:
            cmd = "{}/{}/{}".format(out, p["name"], p["relocate"])
            try:
                subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as e:
                print("relocate error: {}\n{}".format(e, e.output))
                exit(1)

        base = "{}/{}".format(out, p["name"])

        if "env" in p:
            setup_sh.append("")
            setup_sh.append("# {}".format(p["name"]))

            for env in p["env"]:
                value = env["value"].format(base=base)
                if "type" in env:
                    if env["type"] == "list-prepend":
                        value = "{}:${}".format(value, env["var"])
                line = "export {}={}".format(env["var"], value)
                setup_sh.append(line)

    print("Write setup_prebuilt.sh")

    envscript = open("{}/setup_prebuilt.sh".format(options.dest), "w")
    envscript.write("\n".join(setup_sh) + "\n")
    envscript.close()

    print("Done")
