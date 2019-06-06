package ac.kr.hansung.foodsharing;

import android.content.Context;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.widget.LinearLayout;
import android.widget.TextView;

public class ChatOthersView extends LinearLayout {
    TextView userMsg;
    TextView userName;

    public ChatOthersView(Context context) {
        super(context);
        init(context);
    }

    public ChatOthersView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context);
    }

    public void init(Context context) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        inflater.inflate(R.layout.item_chat_others, this, true);

        userMsg = (TextView) findViewById(R.id.textView_chat_others_msg);
        userName = (TextView) findViewById(R.id.textView_chat_others_name);
    }

    public void setMsg(String name) {
        userMsg.setText(name);
    }
    public void setName(String name) {
        userName.setText(name);
    }

}

