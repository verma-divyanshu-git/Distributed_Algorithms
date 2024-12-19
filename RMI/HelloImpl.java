package RMI;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

// Server-side implementation of Hello interface
public class HelloImpl extends UnicastRemoteObject implements Hello {
    public HelloImpl() throws RemoteException {
        super();
    }

    @Override
    public String sayHello() throws RemoteException {
        return "Hello, RMI World!";
    }
}
