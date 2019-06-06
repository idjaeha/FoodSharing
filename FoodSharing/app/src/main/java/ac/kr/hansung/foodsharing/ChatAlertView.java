package ac.kr.hansung.foodsharing;

import android.content.Context;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.widget.LinearLayout;
import android.widget.TextView;

public class ChatAlertView extends LinearLayout {
    TextView alertMsg;

    public ChatAlertView(Context context) {
        super(context);
        init(context);
    }

    public ChatAlertView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context);
    }

    public void init(Context context) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        inflater.inflate(R.layout.item_chat_alert, this, true);

        alertMsg = (TextView) findViewById(R.id.textView_chat_alert_msg);
    }

    public void setMsg(String name) {
        alertMsg.setText(name);
    }

}

