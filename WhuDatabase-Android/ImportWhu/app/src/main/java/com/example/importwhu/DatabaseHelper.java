package com.example.importwhu;
import android.content.Context;
import android.database.Cursor;
//import org.whu.database.SQLiteDatabase;
//import org.whu.database.SQLiteOpenHelper;
import org.sqlite.database.sqlite.SQLiteDatabase;
import org.sqlite.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

public class DatabaseHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "mydatabase.db";
    private static final int DATABASE_VERSION = 1;
    private Context context;

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        this.context = context;
//        loadWhu();
        initializeDatabase();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // 初次创建数据库时，不做任何操作
        // 创建初始表或执行其他初始化操作
        Log.d("Whu", "onCreate");
        loadWhu(db);
        initializeWhuMetaData(db);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // 如果需要更新数据库版本时，处理逻辑
        onCreate(db);
    }

    private void loadWhu(SQLiteDatabase db) {
        String libPath = context.getFilesDir().getAbsolutePath() + "/vec0.so";
        try {
            Cursor c = db.rawQuery("SELECT load_extension('" + libPath + "');", null);
            Log.d("Whu", "Whu extension loaded.");
            c.close();
        } catch (Exception e) {
            Log.e("Whu", "Failed to load Whu extension: " + e.getMessage());
        }
    }


    private void initializeWhuMetaData(SQLiteDatabase db) {
        try {
            // 检查 Whu 元数据是否已经初始化
            Cursor cursor = db.rawQuery("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='spatial_ref_sys';", null);
            if (cursor.moveToFirst() && cursor.getInt(0) == 0) {
                db.rawQuery("SELECT InitSpatialMetaData()", null);
                Log.d("Whu", "Whu metadata initialized.");
            } else {
                Log.d("Whu", "Whu metadata already initialized.");
            }
            cursor.close();
        } catch (Exception e) {
            Log.e("Whu", "Failed to initialize Whu metadata: " + e.getMessage());
        }
    }

    private void initializeDatabase() {
        // 删除现有数据库文件以重新初始化
        context.deleteDatabase(DATABASE_NAME);
        SQLiteDatabase db = this.getWritableDatabase();
        try {
            copyAssetToInternalStorage(context, "vec0.so", context.getFilesDir().getAbsolutePath() + "/vec0.so");
            File file = new File(context.getFilesDir(), "vec0.so");
            if (!file.setExecutable(true)) {
                Log.e("FilePermission", "Failed to set executable permission for vec0.so");
            }
        } catch (IOException e) {
            Log.e("Whu", "Failed to copy Whu extension: " + e.getMessage());
        }
        loadWhu(db);
        initializeWhuMetaData(db);
    }

    private void copyAssetToInternalStorage(Context context, String assetName, String outputPath) throws IOException {
        File outFile = new File(outputPath);
        if (!outFile.exists()) {
            InputStream is = context.getAssets().open(assetName);
            FileOutputStream fos = new FileOutputStream(outFile);
            byte[] buffer = new byte[1024];
            int length;
            while ((length = is.read(buffer)) > 0) {
                fos.write(buffer, 0, length);
            }
            fos.close();
            is.close();
        }
    }

    public void executeSQL(String sql) {
        SQLiteDatabase db = this.getWritableDatabase();
        db.execSQL(sql);
    }

    public Cursor querySQL(String sql) {
        SQLiteDatabase db = this.getReadableDatabase();
        return db.rawQuery(sql, null);
    }
}