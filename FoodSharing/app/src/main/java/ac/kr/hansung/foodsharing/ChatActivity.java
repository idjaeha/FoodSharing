package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Gravity;
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
    public static Handler chatHandler;

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

        chatHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                // 넘어오는 메세지를 이용하여 채팅방 UI를 변경합니다.
                super.handleMessage(msg);
                String command = msg.getData().getString("command");

                if (command.equals("msg")) {
                    String stMsg = msg.getData().getString("msg");
                    String nickName = msg.getData().getString("nick_name");
                    int userNum = msg.getData().getInt("user_num", -1);

                    if (userNum == mobileInfo.userNum) {
                        ChatMyView tmpLayout = new ChatMyView(getApplicationContext());
                        tmpLayout.setMsg(stMsg);
                        layoutChat.addView(tmpLayout);
                    } else {
                        ChatOthersView tmpLayout = new ChatOthersView(getApplicationContext());
                        tmpLayout.setMsg(stMsg);
                        tmpLayout.setName(nickName);
                        layoutChat.addView(tmpLayout);
                    }
                } else  if (command.equals("exit")) {
                    int num = msg.getData().getInt("num");
                    String nickName = msg.getData().getString("nick_name");
                    textViewNum.setText(num + "명");
                    ChatAlertView tmpLayout = new ChatAlertView(getApplicationContext());
                    tmpLayout.setMsg(nickName + " 님이 나가셨습니다.");
                    layoutChat.addView(tmpLayout);
                } else if (command.equals("enter")) {
                    int num = msg.getData().getInt("num");
                    String nickName = msg.getData().getString("nick_name");
                    textViewNum.setText(num + "명");
                    ChatAlertView tmpLayout = new ChatAlertView(getApplicationContext());
                    tmpLayout.setMsg(nickName + " 님이 입장하였습니다.");
                    layoutChat.addView(tmpLayout);
                }
            }
        };

        buttonChat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent msgIntent = new Intent(getApplicationContext(), SocketService.class);
                String tempMsg = editTextChat.getText().toString();
                if (tempMsg.equals("")) {
                    return;
                }
                editTextChat.setText("");
                String msg = "11//" + mobileInfo.userNum + "//" + mobileInfo.nickName + "//" + mobileInfo.foodNum +"//"+ tempMsg + "//";
                msgIntent.putExtra("command", "11");
                msgIntent.putExtra("msg", msg);
                startService(msgIntent);
            }
        });
    }

    @Override
    protected void onStop() {
        super.onStop();
        Intent chatoutIntent = new Intent(this, SocketService.class);
        chatoutIntent.putExtra("command", "13");
        chatoutIntent.putExtra("food_num", mobileInfo.foodNum);
        mobileInfo.foodNum = -1;
        startService(chatoutIntent);
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
