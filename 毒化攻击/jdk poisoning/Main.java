package b;

import javax.tools.JavaCompiler;
//import javax.tools.ToolProvider;
import java.io.File;
import java.lang.ref.Reference;
import java.lang.ref.WeakReference;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import static java.util.logging.Level.FINE;
import static java.util.logging.Level.WARNING;

public class Main {


    private static final String defaultJavaCompilerName
            = "com.sun.tools.javac.api.JavacTool";

    public static void main(String[] args) {
        System.out.println(Main.class.getName()); //b.Main
        //JavaCompiler jc = ToolProvider.getSystemJavaCompiler();  // 把这段代码提取重写出来用于debug
        new Main().getSystemTool(JavaCompiler.class, defaultJavaCompilerName);
    }

    private static final String propertyName = "sun.tools.ToolProvider";
    private static final String loggerName = "javax.tools";
    private static final String[] defaultToolsLocation = {"lib", "tools.jar"};

    private Reference<ClassLoader> refToolClassLoader = null;

    static <T> T trace(Level level, Object reason) {
        // NOTE: do not make this method private as it affects stack traces
        try {
            if (System.getProperty(propertyName) != null) {
                StackTraceElement[] st = Thread.currentThread().getStackTrace();
                String method = "???";
                String cls = Main.class.getName();
                if (st.length > 2) {
                    StackTraceElement frame = st[2];
                    method = String.format((Locale) null, "%s(%s:%s)",
                            frame.getMethodName(),
                            frame.getFileName(),
                            frame.getLineNumber());
                    cls = frame.getClassName();
                }
                Logger logger = Logger.getLogger(loggerName);
                if (reason instanceof Throwable) {
                    logger.logp(level, cls, method,
                            reason.getClass().getName(), (Throwable) reason);
                } else {
                    logger.logp(level, cls, method, String.valueOf(reason));
                }
            }
        } catch (SecurityException ex) {
            System.err.format((Locale) null, "%s: %s; %s%n",
                    Main.class.getName(),
                    reason,
                    ex.getLocalizedMessage());
        }
        return null;
    }

    private <T> T getSystemTool(Class<T> clazz, String name) {
        Class<? extends T> c = getSystemToolClass(clazz, name);
        try {
            return c.asSubclass(clazz).newInstance();
        } catch (Throwable e) {
            trace(WARNING, e);
            return null;
        }
    }

    private Map<String, Reference<Class<?>>> toolClasses = new HashMap<String, Reference<Class<?>>>();

    private <T> Class<? extends T> getSystemToolClass(Class<T> clazz, String name) {
        Reference<Class<?>> refClass = toolClasses.get(name);
        Class<?> c = (refClass == null ? null : refClass.get());
        if (c == null) {
            try {
                c = findSystemToolClass(name);
            } catch (Throwable e) {
                return trace(WARNING, e);
            }
            toolClasses.put(name, new WeakReference<Class<?>>(c));
        }
        return c.asSubclass(clazz);  //clazz  interface javax.tools.JavaCompiler // 校验是否实现了接口,实现接口就不会报错
    }

    private Class<?> findSystemToolClass(String toolClassName)
            throws MalformedURLException, ClassNotFoundException {
        // try loading class directly, in case tool is on the bootclasspath
        try {
            return Class.forName(toolClassName, false, null);
        } catch (ClassNotFoundException e) {
            trace(FINE, e);

            // if tool not on bootclasspath, look in default tools location (tools.jar)
            ClassLoader cl = (refToolClassLoader == null ? null : refToolClassLoader.get());
            if (cl == null) {
                File file = new File(System.getProperty("java.home"));
                if (file.getName().equalsIgnoreCase("jre"))
                    file = file.getParentFile();
                for (String name : defaultToolsLocation)
                    file = new File(file, name);  //file  C:\Program Files (x86)\Java\jdk1.8.0_181\lib\tools.jar

                // if tools not found, no point in trying a URLClassLoader
                // so rethrow the original exception.
                if (!file.exists())
                    throw e;

                URL[] urls = {file.toURI().toURL()};
                trace(FINE, urls[0].toString());

                cl = URLClassLoader.newInstance(urls);
                refToolClassLoader = new WeakReference<ClassLoader>(cl);
            }

            return Class.forName(toolClassName, false, cl);
        }
    }
}
