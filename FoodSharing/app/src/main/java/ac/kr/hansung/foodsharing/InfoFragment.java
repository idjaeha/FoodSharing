package ac.kr.hansung.foodsharing;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;

public class InfoFragment extends Fragment {
    EditText editText_user_x, editText_user_y;
    Button button_user_xy;
    View view;

    public InfoFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        // Inflate the layout for this fragment
        view = inflater.inflate(R.layout.fragment_info, container, false);

        editText_user_x = (EditText) view.findViewById(R.id.editText_user_x);
        editText_user_y = (EditText) view.findViewById(R.id.editText_user_y);
        button_user_xy = (Button) view.findViewById(R.id.button_user_xy);

        editText_user_x.setText(Integer.toString(mobileInfo.getX()));
        editText_user_y.setText(Integer.toString(mobileInfo.getY()));

        button_user_xy.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mobileInfo.setX(Integer.parseInt(editText_user_x.getText().toString()));
                mobileInfo.setY(Integer.parseInt(editText_user_y.getText().toString()));
            }
        });

        return view;
    }

}
