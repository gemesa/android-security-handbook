package com.example.test;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
public class Test {
    private static byte[][] keep;

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
