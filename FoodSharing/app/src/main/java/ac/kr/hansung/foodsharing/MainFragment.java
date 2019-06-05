package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import static ac.kr.hansung.foodsharing.InitActivity.foodInfo;
import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;
import static ac.kr.hansung.foodsharing.SocketService.mySocketService;


public class MainFragment extends Fragment {
    View view;
    FragmentManager fm;
    FragmentTransaction tran;
    ImageView[] category = new ImageView[5];
    int[] category_id = {
            R.id.image_category1,
            R.id.image_category2,
            R.id.image_category3,
            R.id.image_category4,
            R.id.image_category5
    };

    ImageView[] recommend = new ImageView[5];
    int[] recommend_id = {
            R.id.image_recommend1,
            R.id.image_recommend2,
            R.id.image_recommend3,
            R.id.image_recommend4,
            R.id.image_recommend5,
    };

    int[] top5FoodNum = new int[5];

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_main, container, false);

        fm = getActivity().getSupportFragmentManager();
        tran = fm.beginTransaction();

        // 이미지 뷰의 아이디 값을 찾아온다.
        for (int i = 0; i < 5; i++) {
            category[i] = view.findViewById(category_id[i]);
            recommend[i] = view.findViewById(recommend_id[i]);
        }

        setTop5Image();

        //이미지 버튼 설정을 한다.
        for (int i = 0; i < 5; i++) {
            setImageBtn(category[i], category_id[i], i);
            setImageBtn(recommend[i], recommend_id[i], top5FoodNum[i] + 10);
        }

        return view;
    }

    private void setImageBtn(ImageView imgView, int id, final int idx) {
        // 0~4 : 음식 카테고리
        // 10~39 : 음식
        imgView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent socketIntent = new Intent(getActivity(), SocketService.class);

                int flag = idx;
                if (flag >= 0  && flag < 5) {
                    socketIntent.putExtra("command", "5");
                    socketIntent.putExtra("flag", "0");
                    socketIntent.putExtra("category", foodInfo.getCategoryList()[flag]);

                } else if (flag >= 10 && flag < 40) {
                    socketIntent.putExtra("command", "5");
                    socketIntent.putExtra("flag", "1");
                    socketIntent.putExtra("food_name", foodInfo.getFoodList()[flag - 10]);
                }

                mySocketService.processCommand(socketIntent);

            }
        });
    }

    public void setTop5Image() {
        //음식 사진과 top5FoodNum을 설정한다.
        int idx = 0;

        // top5 food를 결정하는 메서드
        Intent socketIntent = new Intent(getActivity(), SocketService.class);
        socketIntent.putExtra("command", "3");
        mySocketService.processCommand(socketIntent);

        // 정보가 아직 업데이트가 안됐다면 기다린다.
        while (mobileInfo.getTop5Food()[0].equals("")) {
        }

        for (int i = 0; i < 5; i++) {
            Log.d("MainFragment", "메뉴 이름 : " + mobileInfo.getTop5Food()[i]);
            // 해당하는 idx를 찾는다.
            for (idx = 0; idx < 30; idx++) {
                if(mobileInfo.getTop5Food()[i].equals(foodInfo.getFoodList()[idx]))
                    break;
            }
            // idx에 맞는 설정을 한다.
            recommend[i].setImageResource(foodInfo.getFoodImgList()[idx]);
            top5FoodNum[i] = idx;

        }
    }
}