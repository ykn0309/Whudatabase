<div style="text-align: center; font-size: 60px; font-weight: bold; font-style: italic; font-family: 'Courier New', Courier, monospace;">
  WhuDatabase-Android
</div>

# 介绍
WhuDatabase-Android是WhuDatabase的安卓版本，是一个可在安卓设备上部署的多模数据库。WhuDatabase-Android目前支持关系型数据、向量型数据、文档型数据以及空间数据。

WhuDatabase-Android基于SQLite实现。SQLite是一个开源的关系型数据库，被广泛应用于手机等嵌入式设备。我们利用SQLite的扩展机制，通过在SQLite运行时加载android-whu-2.0.1扩展，来支持多模数据。下面是对相关扩展的简单介绍：

* android-whu-2.0.1：一个开源的安卓扩展包，可以让SQLite支持向量和空间数据。

# 使用方法

这一部分介绍如何在iOS开发中使用WhuDatabase-iOS。

## 开发工具

* Android Studio：电脑上必须安装Android Studio和相关开发套件。

* 安卓手机：真机测试需要在安卓手机上进行。

## WhuDatabase-Android重要组件

* sqlite3.h：SQLite的头文件。

* android-whu-2.0.1.aar：SQLite的扩展包。

## 快速上手

以真机为例，介绍如何在真实项目中使用WhuDatabase。

### 创建项目

1. 打开Android Studio，选择"Create New Project..."。

    ![打开Xcode](img/image1.png)

2. 选择“Phone and Tablet” -> “Empty Activity”。

    ![选择项目类型](img/image2.png)

3. 输入项目信息，Language选择"Java"，Minimum SDK选择“API 28”。

    ![输入项目信息](img/image3.png)

4. 选择项目保存路径后进入项目。

    ![进入项目](img/image4.png)

5. 连接设备。

    ![alt text](img/image5.png)

6. 点击“▶️”构建并运行项目。确保项目可以在iPhone上成功运行。

    <div style="text-align: center;"><img src="img/image6.jpg" width="30%"></div>

### 配置项目

1. 将项目的视角调整为Project视角

    ![alt text](img/image7.png)

2. 将android-whu-2.0.1.aar扩展包放到/app/libs文件夹下

    ![alt text](img/image8.png)

3. 在build.gradle(:app)中修改三个部分

    * 在dependencies｛｝中添加下列语句。

    ```java
      androidTestImplementation 'androidx.test.espresso:espresso-core:3.3.0'
    ```

    * 在最外层添加下列语句。
    
    ```java
    repositories {
      flatDir {
        dirs 'libs'
      }
    }
    ```

    * 更改compileSdkVersion, targetSdkVersion和minSdkVersion，删掉buildToolsVersion

    ```java
    compileSdkVersion 29
    defaultConfig {
        minSdkVersion 28
        targetSdkVersion 29
    }
    ```

4. 更改之后需要同步build.gradle文件，点击“Sync Now”来同步

    ![alt text](img/image9.png)

5. 点击右上角的SDK Manager并下载API 29，点击Apply以应用到程序中

    ![alt text](img/image10.png)

### 在项目中使用WhuDatabase

1. 在app/src/main/java/com.example.your_project下右键新建一个Java Class并命名为DataBaseHelper

    ![alt text](img/image11.png)

2. 在DatabaseHelper.java中写入以下内容来管理数据库

    ```java
    import android.content.Context;
    import android.database.Cursor;
    import android.util.Log;

    import org.whu.database.SQLiteDatabase;
    import org.whu.database.SQLiteOpenHelper;

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
      }

      @Override
      public void onCreate(SQLiteDatabase db) {
        // 初次创建数据库时，不做任何操作
        // 创建初始表或执行其他初始化操作
        loadWhu(db);
        initializeWhuMetaData(db);
      }

      @Override
      public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // 如果需要更新数据库版本时，处理逻辑
        onCreate(db);
      }

      private void loadWhu(SQLiteDatabase db) {
        try {
            String libPath = context.getFilesDir().getAbsolutePath() + "/libandroid_whu.so";
            db.rawQuery("SELECT load_extension('" + libPath + "')", null);
            Log.d("Whu", "Whu extension loaded.");
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
            copyAssetToInternalStorage(context, "libandroid_whu.so", context.getFilesDir().getAbsolutePath() + "/libandroid_whu.so");
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
    ```

3. 需要在页面上添加两个输入框用来执行数据库创建语句和查询语句，双击src/main/res/layout/activity_main.xml，并点击右上角的split图标，可以看到左边是代码，右边是模拟画面。我们需要在Text中选中Plain Text，并将其拖入模拟画面中，选中边框以调整输入框的大小和位置

    ![alt text](img/image12.png)

4. 将两个EditText的id更改为如图所示，并将text改为hint并输入想要的提示信息

    ![alt text](img/image13.png)

5. 还需要在页面上添加两个按钮来分别执行用户输入的两种语句，在Buttons中选中Button并拖入模拟画面中，选中边框以调整输入框的大小和位置

    ![alt text](img/image14.png)

6. 将两个Button的id更改为如图所示，并将text改为想要显示在按钮上的文字

    ![alt text](img/image15.png)

7. 由于我们整个页面使用的是ConstraintLayout，需要将每个小组件的四条边都固定好。如图所示，我们将第一个EditText的四条边上的圆点连接到了页面的上、左、右以及第一个Button的上边缘，这就代表第一个EditText已经固定好了，另外的组件也用这个方法固定直到红色感叹号消失。固定之后再慢慢调整组件位置

    ![alt text](img/image16.png)
