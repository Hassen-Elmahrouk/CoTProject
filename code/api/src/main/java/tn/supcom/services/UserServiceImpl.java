package tn.supcom.services;



import tn.supcom.exceptions.UserAlreadyExistsException;
import tn.supcom.exceptions.UserNotFoundException;
import tn.supcom.models.User;
import tn.supcom.repository.UserRepository;
import tn.supcom.util.Argon2Utility;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import java.util.List;
import java.util.Optional;

@ApplicationScoped
public class UserServiceImpl  implements  UserService{

    @Inject
    private UserRepository userRepository;
    @Inject
    Argon2Utility argon2Utility ;




    /**
     *
     * @param user
     * @return User
     * @apiNote  THis methode  is used  to create Admin account
     */

    public User createUser(User user){
        if(userRepository.findById(user.getEmail()).isPresent()){
            throw  new UserAlreadyExistsException(user.getEmail()+" is already exists") ;
        }
        user.updatePassword(user.getPassword(),argon2Utility);
        return  userRepository.save(user) ;
    }



    public List<User> findall(){
        return userRepository.findAll();
    }

    /**
     *
     * @param user
     * @return User
     * @throws UserAlreadyExistsException
     * @apiNote  This methode is  used   when the admin add some users to maintain  racks
     */
    @Override
    public User addUser(User user)  {
         if(userRepository.findById(user.getEmail()).isPresent()){
             throw new UserAlreadyExistsException(user.getEmail() +" already exists") ;
         }
         user.updatePassword(user.getPassword(),argon2Utility);
         return userRepository.save(user) ;

    }

    /**
     *
     * @param email
     * @throws  UserNotFoundException
     * @apiNote this methode used by the admin to delete users
     */

    @Override
    public void delete(String email)  {
        if(!userRepository.findById(email).isPresent()){
            throw new UserNotFoundException("there is  no user with email :"+email) ;
        }
        userRepository.deleteById(email);

    }

    @Override
    public Optional<User> getUserById(String email) {
        if(!userRepository.findById(email).isPresent()){
            throw new UserNotFoundException("there is  no user with email :"+email) ;
        }
        return  userRepository.findById(email);


    }
    /**
     * Update user info
     *
     * @param updatedUser The updated user information
     * @return User
     * @throws UserNotFoundException      If the user is not found
     * @throws UserAlreadyExistsException If the updated email already exists for another user
     */
    public User updateUser(User updatedUser) {
        String email = updatedUser.getEmail();

        Optional<User> existingUser = userRepository.findById(email);

        if (existingUser.isPresent()) {
            // Check if the updated email already exists for another user
            userRepository.findByEmail(email).ifPresent(user -> {
                if (!user.getEmail().equals(existingUser.get().getEmail())) {
                    throw new UserAlreadyExistsException("Email " + email + " is already in use by another user.");
                }
            });

            // Perform specific updates or validations here if needed
            // For example, update other fields or perform validations

            // Update the password using the new one provided
            existingUser.get().updatePassword(updatedUser.getPassword(), argon2Utility);

            // Update other fields as needed
            existingUser.get().setSurname(updatedUser.getSurname());
            existingUser.get().setForname(updatedUser.getForname());
            existingUser.get().setRoles(updatedUser.getRoles());

            // Save the updated user
            return userRepository.save(existingUser.get());
        } else {
            throw new UserNotFoundException("User not found with email: " + email);
        }
    }
}
