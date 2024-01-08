package tn.supcom.boundaries;

import tn.supcom.exceptions.UserNotFoundException;
import tn.supcom.filters.Secured;
import tn.supcom.security.Oauth2Request;
import tn.supcom.security.Oauth2Service;

import javax.inject.Inject;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/logout")
@Produces(MediaType.APPLICATION_JSON)
public class LogoutResource {

    @Inject
    private Oauth2Service oauth2Service;

    @DELETE
    @Path("/{email}")
    @Secured
    public Response logoutByEmail(@PathParam("email") String email) {
        try {
            oauth2Service.logout(email);
            return Response.ok("Logout successful").build();
        } catch (UserNotFoundException e) {
            return Response.status(404, e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(500, "Internal Server Error").build();
        }
    }
}
