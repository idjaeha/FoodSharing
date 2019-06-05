package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;
import static ac.kr.hansung.foodsharing.SocketService.mySocketService;

public class ChatActivity extends AppCompatActivity {
    TextView textViewTitle, textViewSubTitle, textViewNum;
    EditText editTextChat;
    Button buttonChat;
    LinearLayout layoutChat;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        textViewNum = findViewById(R.id.textView_chat_num);
        textViewTitle = findViewById(R.id.textView_chat_title);
        textViewSubTitle = findViewById(R.id.textView_chat_subTitle);
        editTextChat = findViewById(R.id.editText_chat);
        buttonChat = findViewById(R.id.button_chat);
        layoutChat = findViewById(R.id.layout_chat);

        buttonChat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent msgIntent = new Intent(getApplicationContext(), SocketService.class);
                String tempMsg = editTextChat.getText().toString();
                editTextChat.setText("");
                String msg = "11//" + mobileInfo.userNum + "//" + mobileInfo.nickName + "//" + mobileInfo.foodNum +"//"+ tempMsg + "//";
                msgIntent.putExtra("command", "11");
                msgIntent.putExtra("msg", msg);
                startService(msgIntent);
            }
        });
    }

    @Override
    protected void onStart() {
        super.onStart();

        Intent infoIntent = getIntent();
        String title = infoIntent.getStringExtra("rest_name");
        String subTitle = infoIntent.getStringExtra("food_name");
        int num = infoIntent.getIntExtra("num", 0);

        textViewTitle.setText(title);
        textViewSubTitle.setText(subTitle);
        textViewNum.setText(Integer.toString(num) + "명");
    }
}
