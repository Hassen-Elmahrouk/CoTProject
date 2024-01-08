package tn.supcom.filters;

import tn.supcom.repository.UserTokenRepository;
import tn.supcom.security.AccessToken;
import tn.supcom.security.UserJWT;


import javax.annotation.Priority;
import javax.inject.Inject;
import javax.security.enterprise.AuthenticationStatus;
import javax.security.enterprise.authentication.mechanism.http.HttpAuthenticationMechanism;
import javax.security.enterprise.authentication.mechanism.http.HttpMessageContext;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.Priorities;
import javax.ws.rs.core.HttpHeaders;
import javax.ws.rs.ext.Provider;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;





@Provider
@Priority(Priorities.AUTHENTICATION)
@Secured

public class AuthenticationFilter implements HttpAuthenticationMechanism {
    private static final Pattern CHALLENGE_PATTERN = Pattern.compile("^Bearer *([^ ]+) *$", Pattern.CASE_INSENSITIVE);
    private  static  final  List NOT_SECURED_PREFIX=List.of("oauth2","signup") ;

    @Inject
    private UserTokenRepository repository;

    @Override
    public AuthenticationStatus validateRequest(HttpServletRequest request, HttpServletResponse response,
                                                HttpMessageContext httpMessageContext) {


        if(!(request.getRequestURI().contains("oauth2")  ||request.getRequestURI().contains("favicon.ico")||request.getRequestURI().contains(".html")|| request.getRequestURI().contains("manifest.json")|| request.getRequestURI().contains("js")|| request.getRequestURI().contains("css")|| request.getRequestURI().contains("png") || request.getRequestURI().contains("signup")||request.getRequestURI().contains("fire"))  ) {
            final String authorization = request.getHeader("Authorization");
            System.out.println(authorization);


            Matcher matcher = CHALLENGE_PATTERN.matcher(Optional.ofNullable(authorization).orElse(""));
            System.out.println(matcher );

            if (!matcher.matches()) {
                return httpMessageContext.responseUnauthorized();
            }

            final String token = matcher.group(1);

            final Optional<AccessToken> optional = repository.findByAccessToken(token)
                    .flatMap(u -> u.findAccessToken(token));
            System.out.println("got the token fromm the db "+ optional);




            if (!optional.isPresent()) {
                return httpMessageContext.responseUnauthorized();
            }


            final AccessToken accessToken = optional.get();
            final Optional<UserJWT> optionalUserJWT = UserJWT.parse(accessToken.getToken(), accessToken.getJwtSecret());
            System.out.println("xhose token is this :" +optionalUserJWT.get().getUser()+  optionalUserJWT.get().getRoles());

            if (optionalUserJWT.isPresent()) {
                final UserJWT userJWT = optionalUserJWT.get();


                return AuthenticationStatus.SUCCESS;
            } else {
                return httpMessageContext.responseUnauthorized();
            }

        }else {
            return  httpMessageContext.doNothing() ;
        }
    }

}