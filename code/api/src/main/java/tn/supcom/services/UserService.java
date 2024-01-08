package tn.supcom.services;


import tn.supcom.exceptions.UserAlreadyExistsException;
import tn.supcom.exceptions.UserNotFoundException;
import tn.supcom.models.User;

import java.util.Optional;

public interface UserService {

    User createUser(User user) throws UserAlreadyExistsException;
    User addUser(User user) throws  UserAlreadyExistsException  ;
    void delete(String email) throws UserNotFoundException;
    // Add new methods for getting user by ID and updating user info
    Optional<User> getUserById(String id) throws UserNotFoundException;

    User updateUser(User user) throws UserNotFoundException, UserAlreadyExistsException;


}
