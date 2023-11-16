import time
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

class AnomalyDetectorIsolationForest:
    def __init__(self, window_size=20):
        """
        Initializes an instance of the AnomalyDetectorIsolationForest class.
        """

        # Set the window size for anomaly detection
        self.window_size = window_size
        
        # Initialize an empty list to store the continuous data stream
        self.data_stream = []

        # Initialize an empty list to store detected anomalies
        self.anomalies = []
        
        # Initialize the Isolation Forest model with a specified contamination level
        self.iforest_model = IsolationForest(contamination=0.05)

    def simulate_data_stream(self):
        """
        Simulates a continuous data stream with synthetic data points, detects anomalies, and visualizes in real-time.
        """

        # Enter an infinite loop for continuous simulation
        while True:
            # Generate a synthetic data point
            data_point = self.generate_data_point()

            # Append the generated data point to the data stream
            self.data_stream.append(data_point)

            # Detect anomalies in the data stream
            self.detect_anomaly(data_point)

            # Visualize the data stream and anomalies in real-time
            self.visualize_data_stream()

            # Pause for one second before the next iteration
            time.sleep(1)

    def generate_data_point(self):
        """
        Generates a synthetic data point with regular patterns, seasonal elements, and random noise.
        """
        
        # Calculate a regular pattern based on a time-dependent factor
        regular_pattern = 10 * (1 + 0.1 * (time.time() % 10))
        # Introduce a seasonal element that varies over time
        seasonal_element = 5 * (1 + 0.5 * ((time.time() % 50) // 10))

        # Add random noise using a Gaussian distribution
        random_noise = random.gauss(0, 1)

        # Combine the components to create a synthetic data point
        data_point = regular_pattern + seasonal_element + random_noise
        return data_point

    def detect_anomaly(self, data_point):
        """
        Detects anomalies in the data stream using the Isolation Forest algorithm.
        """

        # Check if there is enough data for analysis
        if len(self.data_stream) > self.window_size:
            # Create a window of data for analysis
            window_data = np.array(self.data_stream[-self.window_size:]).reshape(-1, 1)

            # Fit the Isolation Forest model with the window data
            self.iforest_model.fit(window_data)

            # Predict anomaly score for the latest data point
            anomaly_score = self.iforest_model.decision_function([[data_point]])

            # Check if the anomaly score is below a threshold
            if anomaly_score < 0:
                # Print a message indicating the index and value of the detected anomaly
                print(len(self.data_stream), f"Anomaly detected: {data_point}", )
                # Append the anomaly information (index, value) to the list of anomalies
                self.anomalies.append((len(self.data_stream), data_point))

    def visualize_data_stream(self):
        """
        Visualizes the data stream in real-time, highlighting anomalies if present.
        - Plots the data stream over time.
        - If anomalies are detected, plots them in red.
        
        """
        
        # Plot the entire data stream
        plt.plot([i for i in range(len(self.data_stream))], self.data_stream, label="Data Stream")
        
        # Check if anomalies are present
        if self.anomalies:
            # Extract x and y coordinates of anomalies
            anomalies_x, anomalies_y = zip(*self.anomalies)

            # Scatter plot anomalies in red with a distinct label
            plt.scatter(anomalies_x, anomalies_y, color='red', label="Anomalies")

        # Add labels and title for better interpretation
        plt.xlabel("Data Point Index")
        plt.ylabel("Data Value")
        plt.title("Real-Time Data Stream Visualization with Anomalies (Isolation Forest)")

        # Display legend to distinguish between data stream and anomalies
        plt.legend()

        # Pause to create a real-time visualization effect
        plt.pause(0.1)

        # Clear the plot for the next iteration
        plt.clf()



if __name__ == "__main__":
    # Create an instance of the AnomalyDetectorIsolationForest class with a window size of 30
    isolation_forest_detector = AnomalyDetectorIsolationForest(window_size=30)

    # Simulate a data stream using the detector
    isolation_forest_detector.simulate_data_stream()

