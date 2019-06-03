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

    ImageView recommend1;
    ImageView recommend2;
    ImageView recommend3;
    ImageView recommend4;
    ImageView recommend5;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_main, container, false);

        fm = getActivity().getSupportFragmentManager();
        tran = fm.beginTransaction();

        for (int i = 0; i < 5; i++) {
            setImageBtn(category[i], category_id[i], i);
        }

        recommend1 = view.findViewById(R.id.image_recommend1);
        recommend2 = view.findViewById(R.id.image_recommend2);
        recommend3 = view.findViewById(R.id.image_recommend3);
        recommend4 = view.findViewById(R.id.image_recommend4);
        recommend5 = view.findViewById(R.id.image_recommend5);

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
}