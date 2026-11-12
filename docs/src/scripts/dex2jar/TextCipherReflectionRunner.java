import java.lang.reflect.Constructor;
import java.lang.reflect.Method;

public class TextCipherReflectionRunner {
    public static void main(String[] args) throws Exception {
        Class<?> c = Class.forName("com.example.test.TextCipher");

        Constructor<?> ctor = c.getDeclaredConstructor();
        ctor.setAccessible(true);                           // needed only when it is private
        Object cipher = ctor.newInstance();

        Method enc = c.getDeclaredMethod("encrypt", String.class);
        enc.setAccessible(true);
        Object result = enc.invoke(cipher, "Hello from the APK!");
        System.out.println(result);

        Method dec = c.getDeclaredMethod("decrypt", String.class);
        dec.setAccessible(true);
        Object back = dec.invoke(cipher, result);
        System.out.println(back);
    }
}
