package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;


public class InitActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_init);
    }

    @Override
    protected void onStart() {
        super.onStart();
        initApp();
    }


    private void initApp() {
        Intent socketIntent = new Intent(this, SocketService.class);
        socketIntent.putExtra("command","1");
        startService(socketIntent);

        //연결이 되면 실행됩니다.
        while (true) {
            //if(socket.isSocketAlive()) {
            Intent intent = new Intent(this, LoginActivity.class);
            startActivityForResult(intent, 101);
            break;
            //}
        }
    }


}