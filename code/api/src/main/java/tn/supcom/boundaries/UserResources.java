package tn.supcom.boundaries;


import tn.supcom.exceptions.UserAlreadyExistsException;
import tn.supcom.exceptions.UserNotFoundException;
import tn.supcom.filters.Secured;
import tn.supcom.models.User;
import tn.supcom.services.UserServiceImpl;

import javax.annotation.security.RolesAllowed;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.validation.Valid;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;


@ApplicationScoped
@Path("")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserResources {

    @Inject
    private UserServiceImpl userService ;

    /**
     *
     * @param
     * @return Response entity
     * @throws  UserAlreadyExistsException
     * @apiNote : used to  create admin account
     */



    @GET
    @Path("/find")
    @RolesAllowed("ADMIN")
    public Response findUsers(){
        System.out.println("find");
        try {
            return Response.ok(userService.findall()).build() ;
        } catch (UserAlreadyExistsException e){
            return  Response.status(400, e.getMessage()).build();
        }


    }

    /**
     *
     * @param user
     * @return Response entity
     * @throws  UserAlreadyExistsException
     * @apiNote : used to  create admin account
     */

    @POST
    @Path("/signup")
    public Response createUser(@Valid User user){
        System.out.println("signup");
         try {
             return Response.ok(userService.createUser(user)).build();
         } catch (UserAlreadyExistsException e){
             return  Response.status(400, e.getMessage()).build();
         }


    }

    /**
     *
     * @param user
     * @return status
     * @apiNote  this methode is used by the admin to add users
     */

    @POST()
    @Path("user/add")
    @Secured
    @RolesAllowed("ADMIN")
    public  Response addUser( @Valid User user){
        try {
            var createdUser = userService.addUser(user);
            return Response.ok(createdUser.getForname() + createdUser.getSurname() + "is added successfully ").build();
        } catch(UserAlreadyExistsException e) {
            return Response.status(400 , e.getMessage()).build() ;

        }

    }


    /**
     *
     * @param email
     * @return status
     * @apiNote  this  methode is used by the Admin to delete users
     */

    @DELETE()
    @Path("user/{email}")
    @RolesAllowed("ADMIN")
    public  Response deleteUser(@PathParam("email") String email){
        try {
              userService.delete(email);
              return  Response.ok().build() ;
        }catch(UserNotFoundException e){
            return  Response.status(400 , e.getMessage()).build() ;
        }

    }
    /**
     * Get user info by email
     *
     * @param email The email of the user
     * @return Response entity
     */
    @GET
    @Path("/user/{email}")
    @RolesAllowed("ADMIN")
    public Response getUserByEmail(@PathParam("email") String email) {
        try {
            User user = userService.getUserById(email)
                    .orElseThrow(() -> new UserNotFoundException("User not found with email: " + email));
            return Response.ok(user).build();
        } catch (UserNotFoundException e) {
            return Response.status(404, e.getMessage()).build();
        }
    }

    /**
     * Update user info
     *
     * @param user The updated user information
     * @return Response entity
     */
    @PUT
    @Path("/user/update")
    @RolesAllowed("ADMIN")
    public Response updateUser(@Valid User user) {
        try {
            User updatedUser = userService.updateUser(user);
            return Response.ok(updatedUser).build();
        } catch (UserNotFoundException e) {
            return Response.status(404, e.getMessage()).build();
        }
    }

    @GET
    @Path("/getAnnotations")
    @RolesAllowed("ADMIN")
    public Response getAnnotationsFromFlaskAPI() {
        try {
            String flaskApiUrl = "http://127.0.0.1:5000/api/annotations";  // Replace with your Flask API URL
            String annotationsJson = sendHttpRequest(flaskApiUrl);

            return Response.ok(annotationsJson).build();
        } catch (IOException e) {
            return Response.status(500, "Error retrieving annotations from Flask API").build();
        }
    }

    private String sendHttpRequest(String apiUrl) throws IOException {
        URL url = new URL(apiUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;

            while ((line = reader.readLine()) != null) {
                response.append(line);
            }

            return response.toString();
        } finally {
            connection.disconnect();
        }
    }




}
