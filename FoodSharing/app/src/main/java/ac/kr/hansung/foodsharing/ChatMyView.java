package ac.kr.hansung.foodsharing;

import android.content.Context;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.widget.LinearLayout;
import android.widget.TextView;

public class ChatMyView extends LinearLayout {
    TextView userMsg;

    public ChatMyView(Context context) {
        super(context);
        init(context);
    }

    public ChatMyView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context);
    }

    public void init(Context context) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        inflater.inflate(R.layout.item_chat_my, this, true);

        userMsg = (TextView) findViewById(R.id.textView_chat_my_msg);
    }

    public void setMsg(String name) {
        userMsg.setText(name);
    }

}

