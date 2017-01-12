import frida, sys, optparse, re
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

jscode = """
Java.perform(function () {
    var currentApplication = Java.use("android.app.ActivityThread").currentApplication();
    var context = currentApplication.getApplicationContext();
    var pkgName = context.getPackageName();
    var dexPath = "%s";
    var entryClass = "%s";
    Java.openClassFile(dexPath).load();
    console.log("inject " + dexPath +" to " + pkgName + " successfully!")
    Java.use(entryClass).%s("%s");
    console.log("call entry successfully!")
});
"""

def checkRequiredArguments(opts, parser):
    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) == None:
            missing_options.extend(option._long_opts)
    if len(missing_options) > 0:
        parser.error('Missing REQUIRED parameters: ' + str(missing_options))

if __name__ == "__main__":
    usage = "usage: python %prog [options] arg\n\n" \
            "example: python %prog -p com.android.launcher " \
            "-f /data/local/tmp/test.apk " \
            "-e com.parker.test.DexMain/main " \
            "\"hello fridex!\""
    parser = optparse.OptionParser(usage)
    parser.add_option("-p", "--package", dest="pkg", type="string",
                      help="[REQUIRED]package name of the app to be injected.")
    parser.add_option("-f", "--file", dest="dexPath", type="string",
                      help="[REQUIRED]path of the dex")
    parser.add_option("-e", "--entry", dest="entry", type="string",
                      help="[REQUIRED]the entry function Name.")

    (options, args) = parser.parse_args()
    checkRequiredArguments(options, parser)
    if len(args) == 0:
        arg = ""
    else:
        arg = args[0]

    pkgName = options.pkg
    dexPath = options.dexPath
    entry = options.entry.split("/")
    if len(entry) > 1:
        entryClass = entry[0]
        entryFunction = entry[1]
    else:
        entryClass = entry[0]
        entryFunction = "main"

    process = frida.get_usb_device().attach(pkgName)
    jscode = jscode%(dexPath, entryClass, entryFunction, arg)
    script = process.create_script(jscode)
    script.on('message', on_message)
    print('[*] Running fridex')
    script.load()
    sys.stdin.read()