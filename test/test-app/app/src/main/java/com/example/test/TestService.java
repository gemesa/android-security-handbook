package com.example.test;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

// https://developer.android.com/develop/background-work/services#java
public class TestService extends Service {
    @Override
    public IBinder onBind(Intent intent) {
        // We don't provide binding, so return null
        return null;
    }
}
