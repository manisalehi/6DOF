import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

#________________________________________________________________________________________________________________________
#                                            2D response visualizer
#________________________________________________________________________________________________________________________ 

#📈 Plotting the response of the system 📈
def ResponsePlotter(solution:dict[str, np.ndarray], title:str):    

    # Setting up the plot 
    fig, axs = plt.subplots(5, 2, figsize=(10,18))
    
    # u - time 
    axs[0,0].plot(solution["times"], solution["states"][:,0])
    axs[0,0].set_title("Response of the u")
    axs[0,0].set_xlabel("Time [s]")
    axs[0,0].set_ylabel("Amplitude")
    axs[0,0].grid()

    # w - time
    axs[0,1].plot(solution["times"], solution["states"][:,1])
    axs[0,1].set_title("Response of the w")
    axs[0,1].set_xlabel("Time [s]")
    axs[0,1].set_ylabel("Amplitude")
    axs[0,1].grid()

    # q - time
    axs[1,0].plot(solution["times"], solution["states"][:,2])
    axs[1,0].set_title("Response of the q")
    axs[1,0].set_xlabel("Time [s]")
    axs[1,0].set_ylabel("Amplitude")
    axs[1,0].grid()

    # θ - time
    axs[1,1].plot(solution["times"], solution["states"][:,3])
    axs[1,1].set_title("Response of the θ")
    axs[1,1].set_xlabel("Time [s]")
    axs[1,1].set_ylabel("Amplitude")
    axs[1,1].grid()

    # v - time
    axs[2,0].plot(solution["times"], solution["states"][:,4])
    axs[2,0].set_title("Response of the v")
    axs[2,0].set_xlabel("Time [s]")
    axs[2,0].set_ylabel("Amplitude")
    axs[2,0].grid()

    # p - time
    axs[2,1].plot(solution["times"], solution["states"][:,5])
    axs[2,1].set_title("Response of the p")
    axs[2,1].set_xlabel("Time [s]")
    axs[2,1].set_ylabel("Amplitude")
    axs[2,1].grid()

    # r - time
    axs[3,0].plot(solution["times"], solution["states"][:,6])
    axs[3,0].set_title("Response of the r")
    axs[3,0].set_xlabel("Time [s]")
    axs[3,0].set_ylabel("Amplitude")
    axs[3,0].grid()

    # φ - time
    axs[3,1].plot(solution["times"], solution["states"][:,7])
    axs[3,1].set_title("Response of the φ")
    axs[3,1].set_xlabel("Time [s]")
    axs[3,1].set_ylabel("Amplitude")
    axs[3,1].grid()

    # ψ - time
    axs[4,0].plot(solution["times"], solution["states"][:,8])
    axs[4,0].set_title("Response of the ψ")
    axs[4,0].set_xlabel("Time [s]")
    axs[4,0].set_ylabel("Amplitude")
    axs[4,0].grid()

    fig.suptitle(title + "\n ", size=20)
    fig.subplots_adjust(top=0.2)
    fig.delaxes(axs[4][1])  # Removing the 10th plot
    fig.tight_layout()      # Making the spacing to look good


#📈 Plotting the response of the system 📈
def Position2D(solution:dict[str, np.ndarray], title:str):    
    # Setting up the plot 
    fig, axs = plt.subplots(3, 1, figsize=(8,10))
    
    # x_NED - time 
    axs[0].plot(solution["times"], solution["positions"][:,0])
    axs[0].set_title("x_NED [m]")
    axs[0].set_xlabel("Time [s]")
    axs[0].set_ylabel("Amplitude")
    axs[0].grid()

    # y_NED - time 
    axs[1].plot(solution["times"], solution["positions"][:,0])
    axs[1].set_title("y_NED [m]")
    axs[1].set_xlabel("Time [s]")
    axs[1].set_ylabel("Amplitude")
    axs[1].grid()

    # z_NED - time 
    axs[2].plot(solution["times"], solution["positions"][:,0])
    axs[2].set_title("z_NED [m]")
    axs[2].set_xlabel("Time [s]")
    axs[2].set_ylabel("Amplitude")
    axs[2].grid()

    fig.suptitle(title + "\n ", size=20)
    fig.tight_layout()      # Making the spacing to look good


#📈 Plotting the response of the system 📈
def Position3D(solution:dict[str, np.ndarray], title:str = "3D Trajectory"):    
    
    # Create the 3D trajectory plot
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x = solution["positions"][:,0],
                y = solution["positions"][:,1],
                z = solution["positions"][:,2],
                mode='lines+markers',   # shows both line + points
                line=dict(width=4),
                marker=dict(size=3)
            )
        ]
    )

    # Layout (optional)
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        title=title
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=True, showgrid=True, zeroline=False),
            yaxis=dict(showbackground=True, showgrid=True, zeroline=False),
            zaxis=dict(showbackground=True, showgrid=True, zeroline=False),
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # remove outside borders
    )

    fig.show()



