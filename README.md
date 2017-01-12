# fridex
a frida script for inject dex
```
Usage: python fridex.py [options] arg

example: python fridex.py -p com.android.launcher -f /data/local/tmp/test.apk -e com.parker.test.DexMain/main "hello fridex!"

Options:
  -h, --help            show this help message and exit
  -p PKG, --package=PKG
                        [REQUIRED]package name of the app to be injected.
  -f DEXPATH, --file=DEXPATH
                        [REQUIRED]path of the dex
  -e ENTRY, --entry=ENTRY
                        [REQUIRED]the entry function Name.
```

the entry function name of dex should be like this:
```Java
public class DexMain {
    public static void main(String arg) {
        Log.d("parker", "arg is " + arg);
    }
}
```