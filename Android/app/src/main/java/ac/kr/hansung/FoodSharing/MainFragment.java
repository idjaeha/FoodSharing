package ac.kr.hansung.FoodSharing;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class MainFragment extends Fragment {
    View view;
    BitmapButton bitmapButton;
    FragmentManager fm;
    FragmentTransaction tran;
    StoreListFragment storeListFragment;
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_main, container, false);

        bitmapButton = (BitmapButton) getActivity().findViewById(R.id.bitmapButton1);
        storeListFragment = new StoreListFragment();
        fm = getActivity().getSupportFragmentManager();
        tran = fm.beginTransaction();
        /*
        bitmapButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                tran.replace(R.id.frag_frame, storeListFragment);
                tran.commit();
            }
        });
        */

        return view;
    }
}