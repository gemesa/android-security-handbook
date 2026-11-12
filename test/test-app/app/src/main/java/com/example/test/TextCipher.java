package com.example.test;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
public class TextCipher {
    private final byte KEY = 0x5A;

    public String encrypt(String plain) {
        byte[] data = xor(plain.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(data);
    }

    public String decrypt(String encoded) {
        byte[] data = xor(Base64.getDecoder().decode(encoded));
        return new String(data, StandardCharsets.UTF_8);
    }

    private byte[] xor(byte[] in) {
        byte[] out = new byte[in.length];
        for (int i = 0; i < in.length; i++) {
            out[i] = (byte) (in[i] ^ KEY);
        }
        return out;
    }
}
