package com.example.importwhu;
import android.database.Cursor;
import org.whu.database.SQLiteDatabase;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;


public class MainActivity extends AppCompatActivity {

    private DatabaseHelper dbHelper;
    private EditText editTextSQL1, editTextSQL2;
    private TextView textViewResults;

    static {
        System.loadLibrary("sqliteX");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        dbHelper = new DatabaseHelper(this);
        editTextSQL1 = findViewById(R.id.editTextSQL1);
        editTextSQL2 = findViewById(R.id.editTextSQL2);
        textViewResults = findViewById(R.id.textViewResults);
        Button buttonExecute1 = findViewById(R.id.buttonExecute1);
        Button buttonExecute2 = findViewById(R.id.buttonExecute2);

        buttonExecute1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String sql1 = editTextSQL1.getText().toString().trim();

                if (sql1.toLowerCase().startsWith("select")) {
                    queryAndDisplayResults(sql1);
                } else {
                    try {
                        dbHelper.executeSQL(sql1);
                        Toast.makeText(MainActivity.this, "SQL executed successfully", Toast.LENGTH_SHORT).show();
                    } catch (Exception e) {
                        Toast.makeText(MainActivity.this, "SQL execution failed: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        buttonExecute2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String sql2 = editTextSQL2.getText().toString().trim();

                try {
                    Cursor cursor = dbHelper.querySQL(sql2);
                    StringBuilder stringBuilder = new StringBuilder();

                    // 获取列名
                    String[] columnNames = cursor.getColumnNames();
                    for (String columnName : columnNames) {
                        stringBuilder.append(columnName).append("\t");
                    }
                    stringBuilder.append("\n");

                    // 获取数据
                    while (cursor.moveToNext()) {
                        for (String columnName : columnNames) {
                            stringBuilder.append(cursor.getString(cursor.getColumnIndexOrThrow(columnName))).append("\t");
                        }
                        stringBuilder.append("\n");
                    }

                    textViewResults.setText(stringBuilder.toString());
                    Toast.makeText(MainActivity.this, "Query executed successfully", Toast.LENGTH_SHORT).show();
                    cursor.close();
                } catch (Exception e) {
                    Toast.makeText(MainActivity.this, "Query execution failed: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void queryAndDisplayResults(String sql) {
        try {
            Cursor cursor = dbHelper.querySQL(sql);
            StringBuilder stringBuilder = new StringBuilder();

            // 获取列名
            String[] columnNames = cursor.getColumnNames();
            for (String columnName : columnNames) {
                stringBuilder.append(columnName).append("\t");
            }
            stringBuilder.append("\n");

            // 获取数据
            while (cursor.moveToNext()) {
                for (String columnName : columnNames) {
                    stringBuilder.append(cursor.getString(cursor.getColumnIndexOrThrow(columnName))).append("\t");
                }
                stringBuilder.append("\n");
            }

            textViewResults.setText(stringBuilder.toString());
            cursor.close();
        } catch (Exception e) {
            Toast.makeText(MainActivity.this, "Query execution failed: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }
}