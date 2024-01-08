package tn.supcom;

import tn.supcom.boundaries.UserResources;
import tn.supcom.filters.CorsFilter;

import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;
import java.util.HashSet;
import java.util.Set;

@ApplicationPath("/api")
public class JAXRSConfiguration extends Application {
}
