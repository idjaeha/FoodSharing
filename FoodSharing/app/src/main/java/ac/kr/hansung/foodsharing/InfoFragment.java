package ac.kr.hansung.foodsharing;


import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;
import static ac.kr.hansung.foodsharing.SocketService.mySocketService;

public class InfoFragment extends Fragment {
    EditText editText_user_x, editText_user_y, editText_user_nickname;
    Button button_user_check, button_info_1, button_info_2, button_info_3, button_info_4, button_info_5, button_info_6;
    View view;

    public InfoFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(final LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        // Inflate the layout for this fragment
        view = inflater.inflate(R.layout.fragment_info, container, false);

        editText_user_x = (EditText) view.findViewById(R.id.editText_user_x);
        editText_user_y = (EditText) view.findViewById(R.id.editText_user_y);
        editText_user_nickname = view.findViewById(R.id.editText_user_nickname);
        button_info_1 = view.findViewById(R.id.button_info_1);
        button_info_2 = view.findViewById(R.id.button_info_2);
        button_info_3 = view.findViewById(R.id.button_info_3);
        button_info_4 = view.findViewById(R.id.button_info_4);
        button_info_5 = view.findViewById(R.id.button_info_5);
        button_info_6 = view.findViewById(R.id.button_info_6);

        button_user_check = (Button) view.findViewById(R.id.button_user_check);

        editText_user_x.setText(Integer.toString(mobileInfo.getX()));
        editText_user_y.setText(Integer.toString(mobileInfo.getY()));
        editText_user_nickname.setText(mobileInfo.nickName);

        button_user_check.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mobileInfo.setX(Integer.parseInt(editText_user_x.getText().toString()));
                mobileInfo.setY(Integer.parseInt(editText_user_y.getText().toString()));
                mobileInfo.setNickName(editText_user_nickname.getText().toString());
            }
        });

        button_info_1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), SocketService.class);
                intent.putExtra("command", "100");
                intent.putExtra("category", "1");
                mySocketService.processCommand(intent);
            }
        });

        button_info_2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), SocketService.class);
                intent.putExtra("command", "100");
                intent.putExtra("category", "2");
                mySocketService.processCommand(intent);
            }
        });

        button_info_3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), SocketService.class);
                intent.putExtra("command", "100");
                intent.putExtra("category", "3");
                mySocketService.processCommand(intent);
            }
        });

        button_info_4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), SocketService.class);
                intent.putExtra("command", "100");
                intent.putExtra("category", "4");
                mySocketService.processCommand(intent);
            }
        });

        button_info_5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), SocketService.class);
                intent.putExtra("command", "100");
                intent.putExtra("category", "5");
                mySocketService.processCommand(intent);
            }
        });

        button_info_6.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), SocketService.class);
                intent.putExtra("command", "100");
                intent.putExtra("category", "6");
                mySocketService.processCommand(intent);
            }
        });

        return view;
    }

}
