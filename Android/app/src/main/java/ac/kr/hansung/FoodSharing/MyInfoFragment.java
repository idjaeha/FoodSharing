package ac.kr.hansung.FoodSharing;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;

public class MyInfoFragment extends Fragment {
    View rootView;
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        rootView = inflater.inflate(R.layout.fragment_my_info, container, false);
        getProfile();
        return rootView;
    }

    public void getProfile() {
        GoogleSignInAccount user = GoogleSignIn.getLastSignedInAccount(rootView.getContext());
        if (user != null) {
                String id = user.getId();
                String name = user.getDisplayName();
                String email = user.getEmail();
                Uri photoUrl = user.getPhotoUrl();

                TextView id_view = (TextView) rootView.findViewById(R.id.id_myinfo);
                TextView name_view = (TextView) rootView.findViewById(R.id.name_myinfo);
                TextView email_view = (TextView) rootView.findViewById(R.id.email_myinfo);

                id_view.setText(id);
                name_view.setText(name);
                email_view.setText(email);
        }
        else {
            Intent intent = new Intent(rootView.getContext(), LoginActivity.class);
            startActivityForResult(intent, 101);
        }
    }
}