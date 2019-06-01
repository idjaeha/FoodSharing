package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }

    @Override
    protected void onStart() {
        super.onStart();
        LoginApp();
    }


    private void LoginApp() {

        //Intent intent = new Intent(this, LoginActivity.class);
        Intent intent = new Intent(this, MainActivity.class);
        startActivityForResult(intent, 101);
    }
}