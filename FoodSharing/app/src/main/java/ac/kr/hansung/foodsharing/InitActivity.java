package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import static ac.kr.hansung.foodsharing.SocketService.addr;
import static ac.kr.hansung.foodsharing.SocketService.mySocketService;
import static ac.kr.hansung.foodsharing.SocketService.port;


public class InitActivity extends AppCompatActivity {
    public static MobileInfo mobileInfo;
    public static FoodInfo foodInfo;
    EditText editTextIP, editTextPort;
    Button buttonConnect;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_init);

        editTextIP = findViewById(R.id.editText_ip);
        editTextPort = findViewById(R.id.editText_port);
        buttonConnect = findViewById(R.id.button_connect);
        buttonConnect.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                addr = editTextIP.getText().toString();
                port = Integer.parseInt(editTextPort.getText().toString());
                connectServer(false);
            }
        });

        mobileInfo = new MobileInfo(0, "","");
        foodInfo = new FoodInfo();
    }

    @Override
    protected void onStart() {
        Log.d("InitActivity","Init mobile");
        super.onStart();
        //initApp();
    }

    private void initApp() {
        connectServer(true);
    }

    public void connectServer(boolean flag) {
        if(!flag) {
            Log.d("InitActivity", "Socket 생성 요청");
            Intent socketIntent = new Intent(getApplicationContext(), SocketService.class);
            startService(socketIntent);

            Log.d("InitActivity", "서버 연결 확인");
            Intent connectIntent = new Intent(getApplicationContext(), SocketService.class);
            connectIntent.putExtra("command", "0");
            startService(connectIntent);

            Log.d("InitActivity", "서버 연결 요청");
            if (mobileInfo.isConnectServer) {
                Intent intent = new Intent(getApplicationContext(), LoginActivity.class);
                startActivityForResult(intent, 101);
            }
        } else {
            Log.d("InitActivity", "Socket 생성 요청");
            Intent socketIntent = new Intent(getApplicationContext(), SocketService.class);
            startService(socketIntent);

            Log.d("InitActivity", "서버 연결 확인");
            Intent connectIntent = new Intent(getApplicationContext(), SocketService.class);
            connectIntent.putExtra("command", "0");
            startService(connectIntent);

            Log.d("InitActivity", "서버 연결 요청");
            Intent intent = new Intent(getApplicationContext(), LoginActivity.class);
            startActivityForResult(intent, 101);

        }
    }


}