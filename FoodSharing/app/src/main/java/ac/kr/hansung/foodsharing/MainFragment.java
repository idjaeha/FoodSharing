package ac.kr.hansung.foodsharing;

import android.content.Intent;
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

import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;


public class MainFragment extends Fragment {
    private static final int[] category_request = {
            200, 201, 202, 203, 204
    };
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

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_main, container, false);

        fm = getActivity().getSupportFragmentManager();
        tran = fm.beginTransaction();

        for (int i = 0; i < 5; i++) {
            setImageBtn(category[i], category_id[i], i);
        }

        for (int i = 0; i < 5; i++) {
            recommend[i] = view.findViewById(recommend_id[i]);
        }
        recommend[2].setImageResource(R.drawable.image_bibim);

        setTop5Image();

        return view;
    }

    private void setImageBtn(ImageView imgView, int id, final int idx) {
        imgView = view.findViewById(id);
        imgView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), StoreListActivity.class);
                intent.putExtra("category", idx);
                startActivityForResult(intent, category_request[idx]);
            }
        });
    }

    public void setTop5Image() {
        for (int i = 0; i < 5; i++) {
            Log.d("MainActivity", "메뉴 이름 : " + mobileInfo.getTop5Food()[i]);
            if (mobileInfo.getTop5Food()[i].equals("비빔밥"))
                recommend[i].setImageResource(R.drawable.image_bibim);
            else if (mobileInfo.getTop5Food()[i].equals("불고기"))
                recommend[i].setImageResource(R.drawable.image_bulgogi);
            else if (mobileInfo.getTop5Food()[i].equals("된장찌개"))
                recommend[i].setImageResource(R.drawable.image_damnzang);
            else if (mobileInfo.getTop5Food()[i].equals("김치찌개"))
                recommend[i].setImageResource(R.drawable.image_gimchi);
            else if (mobileInfo.getTop5Food()[i].equals("김치전"))
                recommend[i].setImageResource(R.drawable.image_gimchijun);
            else if (mobileInfo.getTop5Food()[i].equals("떡갈비"))
                recommend[i].setImageResource(R.drawable.image_dduckgalbi);
            else if (mobileInfo.getTop5Food()[i].equals("자장면"))
                recommend[i].setImageResource(R.drawable.image_zazang);
            else if (mobileInfo.getTop5Food()[i].equals("짬뽕"))
                recommend[i].setImageResource(R.drawable.image_zzamgbbong);
            else if (mobileInfo.getTop5Food()[i].equals("탕수육"))
                recommend[i].setImageResource(R.drawable.image_tang);
            else if (mobileInfo.getTop5Food()[i].equals("깐풍기"))
                recommend[i].setImageResource(R.drawable.image_kkan);
            else if (mobileInfo.getTop5Food()[i].equals("팔보채"))
                recommend[i].setImageResource(R.drawable.image_palbo);
            else if (mobileInfo.getTop5Food()[i].equals("칠리새우"))
                recommend[i].setImageResource(R.drawable.image_chill);
            else if (mobileInfo.getTop5Food()[i].equals("파스타"))
                recommend[i].setImageResource(R.drawable.image_pasta);
            else if (mobileInfo.getTop5Food()[i].equals("스테이크"))
                recommend[i].setImageResource(R.drawable.image_steak);
            else if (mobileInfo.getTop5Food()[i].equals("샐러드"))
                recommend[i].setImageResource(R.drawable.image_salad);
            else if (mobileInfo.getTop5Food()[i].equals("오믈렛"))
                recommend[i].setImageResource(R.drawable.image_omlet);
            else if (mobileInfo.getTop5Food()[i].equals("햄버거"))
                recommend[i].setImageResource(R.drawable.image_hamberger);
            else if (mobileInfo.getTop5Food()[i].equals("피자"))
                recommend[i].setImageResource(R.drawable.image_pizza);
            else if (mobileInfo.getTop5Food()[i].equals("초밥"))
                recommend[i].setImageResource(R.drawable.image_chobob);
            else if (mobileInfo.getTop5Food()[i].equals("가츠동"))
                recommend[i].setImageResource(R.drawable.image_gachdong);
            else if (mobileInfo.getTop5Food()[i].equals("우동"))
                recommend[i].setImageResource(R.drawable.image_udong);
            else if (mobileInfo.getTop5Food()[i].equals("텐동"))
                recommend[i].setImageResource(R.drawable.image_tendong);
            else if (mobileInfo.getTop5Food()[i].equals("라멘"))
                recommend[i].setImageResource(R.drawable.image_ramen);
            else if (mobileInfo.getTop5Food()[i].equals("사시미"))
                recommend[i].setImageResource(R.drawable.image_sashimi);
            else if (mobileInfo.getTop5Food()[i].equals("떡볶이"))
                recommend[i].setImageResource(R.drawable.image_dduckbok);
            else if (mobileInfo.getTop5Food()[i].equals("김밥"))
                recommend[i].setImageResource(R.drawable.image_gimbob);
            else if (mobileInfo.getTop5Food()[i].equals("튀김"))
                recommend[i].setImageResource(R.drawable.image_thigim);
            else if (mobileInfo.getTop5Food()[i].equals("순대"))
                recommend[i].setImageResource(R.drawable.image_soondae);
            else if (mobileInfo.getTop5Food()[i].equals("오뎅"))
                recommend[i].setImageResource(R.drawable.image_odang);
            else if (mobileInfo.getTop5Food()[i].equals("주먹밥"))
                recommend[i].setImageResource(R.drawable.image_punchbob);


        }
    }
}