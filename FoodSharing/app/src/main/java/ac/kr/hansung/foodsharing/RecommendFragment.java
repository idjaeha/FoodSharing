package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import static ac.kr.hansung.foodsharing.InitActivity.foodInfo;
import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;
import static ac.kr.hansung.foodsharing.SocketService.mySocketService;


public class RecommendFragment extends Fragment {
    View view;

    ImageView[] imageViewsRecommend = new ImageView[5];
    int[] recommend_id = {
            R.id.imageView_recommend_1,
            R.id.imageView_recommend_2,
            R.id.imageView_recommend_3,
            R.id.imageView_recommend_4,
            R.id.imageView_recommend_5,
    };

    int[] top5FoodNum = new int[5];

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_recommend, container, false);

        // 이미지 뷰의 아이디 값을 찾아온다.
        for (int i = 0; i < 5; i++) {
            imageViewsRecommend[i] = view.findViewById(recommend_id[i]);
        }

        setTop5Image();

        //이미지 버튼 설정을 한다.
        for (int i = 0; i < 5; i++) {
            setImageBtn(imageViewsRecommend[i], recommend_id[i], top5FoodNum[i]);
        }

        return view;
    }

    private void setImageBtn(ImageView imgView, int id, final int idx) {
        // 0~29 : 음식 카테고리
        imgView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent socketIntent = new Intent(getActivity(), SocketService.class);
                int flag = idx;
                socketIntent.putExtra("command", "5");
                socketIntent.putExtra("flag", "1");
                socketIntent.putExtra("food_name", foodInfo.getFoodList()[flag]);
                mySocketService.processCommand(socketIntent);
            }
        });
    }

    public void setTop5Image() {
        //음식 사진과 top5FoodNum을 설정한다.
        int idx = 0;

        // top5 food를 결정하는 메서드
        Intent socketIntent = new Intent(getActivity(), SocketService.class);
        socketIntent.putExtra("command", "15");
        socketIntent.putExtra("user_num", mobileInfo.userNum);
        mySocketService.processCommand(socketIntent);

        // 정보가 아직 업데이트가 안됐다면 기다린다.
        while (mobileInfo.getUserTop5Food()[0].equals("")) {
        }

        for (int i = 0; i < 5; i++) {
            Log.d("RecommendFragment", "메뉴 이름 : " + mobileInfo.getUserTop5Food()[i]);
            // 해당하는 idx를 찾는다.
            for (idx = 0; idx < 30; idx++) {
                if(mobileInfo.getUserTop5Food()[i].equals(foodInfo.getFoodList()[idx]))
                    break;
            }
            // idx에 맞는 설정을 한다.
            imageViewsRecommend[i].setImageResource(foodInfo.getFoodImgList()[idx]);
            top5FoodNum[i] = idx;

        }
    }
}
