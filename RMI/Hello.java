package RMI;

import java.rmi.Remote;
import java.rmi.RemoteException;

// Remote interface
public interface Hello extends Remote {
    String sayHello() throws RemoteException;
}
