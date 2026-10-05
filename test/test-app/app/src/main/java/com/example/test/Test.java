package com.example.test;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.security.cert.Certificate;
import java.util.ArrayList;
import java.util.List;

import okhttp3.CertificatePinner;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

// References:
// https://developer.android.com/guide/components/processes-and-threads
// https://developer.android.com/reference/android/os/NetworkOnMainThreadException
// https://developer.android.com/reference/android/app/Activity#runOnUiThread(java.lang.Runnable)
// https://developer.android.com/develop/ui/views/touch-and-input/input-events#java
// https://developer.android.com/reference/java/lang/Thread#start()
// https://developer.android.com/reference/android/widget/Button
// https://developer.android.com/reference/android/widget/TextView
// https://developer.android.com/reference/kotlin/androidx/constraintlayout/widget/ConstraintLayout
// https://github.com/lysine-dev/okhttp

public class Test {
    static {
        System.loadLibrary("native-lib");
    }

    public static native String stringFromNative();

    private static byte[][] keep;

    // A simple HTTP Request & Response Service.
    private static final String HOSTNAME = "httpbin.org";
    private static final String SERVER_URL = "https://" + HOSTNAME + "/get";

    // $ curl -sv --pinnedpubkey "sha256//AAA=" https://httpbin.org/get 2>&1 | grep "public key hash"
    //*  public key hash: sha256//AxBkYmhbMwxqUkEu7yx5FyIaTOfXqiqMYahybvzFxfw=
    // $ curl --pinnedpubkey "sha256//AxBkYmhbMwxqUkEu7yx5FyIaTOfXqiqMYahybvzFxfw=" https://httpbin.org/get
    // okhttp format // --> /
    private static final String PIN = "sha256/AxBkYmhbMwxqUkEu7yx5FyIaTOfXqiqMYahybvzFxfw=";

    // https://lysine.dev/okhttp/features/https/#__tabbed_1_2
    private static final OkHttpClient client = new OkHttpClient.Builder()
            .certificatePinner(
                    new CertificatePinner.Builder()
                            .add(HOSTNAME,PIN)
                            .build())
            .build();

    public static List<String> fetch() throws Exception {
        List<String> results = new ArrayList<>();
        Request request = new Request.Builder()
                .url(SERVER_URL)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

            results.add(response.toString());
            results.add("Pin: " + PIN);
            for (Certificate certificate : response.handshake().peerCertificates()) {
                results.add("Peer: " + CertificatePinner.pin(certificate));
            }
            return results;
        }
    }
    public static void init() {
        int x = 285735461;
        String s = Integer.toString(x);

        keep = new byte[][] {
                s.getBytes(StandardCharsets.US_ASCII),
                s.getBytes(StandardCharsets.UTF_16LE),
                s.getBytes(StandardCharsets.UTF_16BE),
                ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(x).array(),
                ByteBuffer.allocate(4).order(ByteOrder.BIG_ENDIAN).putInt(x).array(),
                ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN).putLong(x).array(),
                ByteBuffer.allocate(8).order(ByteOrder.BIG_ENDIAN).putLong(x).array(),
                { 0x28, 0x57, 0x35, 0x46, 0x10},
                { 0x10, 0x46, 0x35, 0x57, 0x28 }
        };
    }
}
