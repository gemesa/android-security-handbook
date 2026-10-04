package com.example.test;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.util.ArrayList;
import java.util.List;


public class MainActivity extends AppCompatActivity {

    private TextView resultText;
    private TextView certText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        Test.init();
        startService(new Intent(this, Worker1.class));
        startService(new Intent(this, Worker2.class));

        resultText = findViewById(R.id.resultText);
        certText = findViewById(R.id.certText);
        Button fetchButton = findViewById(R.id.fetchButton);
        fetchButton.setOnClickListener(this::onFetchClicked);
    }

    private void onFetchClicked(View v) {
        resultText.setText("");
        certText.setText("");
        new Thread(this::fetchInBackground).start();
    }

    // Runs on the background thread.
    private void fetchInBackground() {
        List<String> result = new ArrayList<>();
        try {
            result = Test.fetch();
        } catch (Exception e) {
            result.add(e.toString());
        }
        String text1 = result.get(0);
        runOnUiThread(() -> resultText.setText(text1));
        String text2 = String.join("\n", result.subList(1, result.size()));
        runOnUiThread(() -> certText.setText(text2));
    }

}