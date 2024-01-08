package tn.supcom.filters;

import javax.enterprise.util.AnnotationLiteral;
import javax.inject.Qualifier;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.util.logging.Logger;

@Qualifier
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.FIELD, ElementType.METHOD, ElementType.TYPE, ElementType.PARAMETER})
public @interface MyLogger {
    class Literal extends AnnotationLiteral<MyLogger> implements MyLogger {
        public static final Literal INSTANCE = new Literal();
    }
}