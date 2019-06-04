package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import static ac.kr.hansung.foodsharing.InitActivity.foodInfo;
import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;


public class LoginActivity extends AppCompatActivity {
    Button loginButton;
    EditText editTextId;
    EditText editTextPwd;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        editTextId = findViewById(R.id.editText_id);
        editTextPwd = findViewById(R.id.editText_pwd);

        loginButton = findViewById(R.id.button_login);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LoginApp();
            }
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
    }


    private void LoginApp() {
        CheckID();
        editTextId.setText("");
        editTextPwd.setText("");
    }

    private  void CheckID() {
        Intent socketIntent = new Intent(this, SocketService.class);
        socketIntent.putExtra("command", "1");
        socketIntent.putExtra("id", editTextId.getText().toString());
        socketIntent.putExtra("pwd", editTextPwd.getText().toString());
        startService(socketIntent);
    }
}