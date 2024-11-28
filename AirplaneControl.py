import tkinter as tk
import math


class AirplaneSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Airplane Trajectory Visualization")
        self.mWidth = 800
        self.mHeight = 800
        # Create the canvas for visualization
        self.canvas = tk.Canvas(root, width=self.mWidth, height=self.mHeight, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=6)

        # Initial airplane state
        self.x = self.mWidth//2  # Initial x-coordinate
        self.y = self.mHeight//2  # Initial y-coordinate
        self.angle = 0  # Yaw angle in degrees
        self.speed_knots = 0  # Airspeed in knots
        self.speed_pixels = 0  # Airspeed in pixels per update
        self.trail = []  # List to store trajectory points

        # Draw the initial airplane position
        self.airplane = self.canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill="red")

        # Control panel for yaw and airspeed
        tk.Label(root, text="Yaw Angle (-180 to 180):").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.angle_slider = tk.Scale(root, from_=-180, to=180, orient="horizontal", command=self.update_angle)
        self.angle_slider.set(0)
        self.angle_slider.grid(row=0, column=2, pady=5)

        self.angle_value = tk.Label(root, text="Current Yaw: 0°")
        self.angle_value.grid(row=0, column=3, padx=10)

        tk.Label(root, text="Airspeed (knots):").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.speed_slider = tk.Scale(root, from_=0, to=200, orient="horizontal", command=self.update_speed)
        self.speed_slider.set(0)
        self.speed_slider.grid(row=1, column=2, pady=5)

        self.speed_value = tk.Label(root, text="Current Speed: 0 knots")
        self.speed_value.grid(row=1, column=3, padx=10)

        # Labels and Entry fields for manual input (organized near Update Controls button)
        control_frame = tk.Frame(root)
        control_frame.grid(row=2, column=1, columnspan=3, pady=10, padx=10)

        tk.Label(control_frame, text="Yaw Angle:").grid(row=0, column=0, padx=5)
        self.angle_input = tk.Entry(control_frame)
        self.angle_input.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Airspeed (knots):").grid(row=1, column=0, padx=5)
        self.speed_input = tk.Entry(control_frame)
        self.speed_input.grid(row=1, column=1, padx=5)

        # Update button
        self.update_button = tk.Button(control_frame, text="Update Controls", command=self.update_controls)
        self.update_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Start/Stop/Reset buttons
        self.start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=4, column=1, columnspan=2, pady=5)

        self.stop_button = tk.Button(root, text="Stop Simulation", command=self.stop_simulation, state="disabled")
        self.stop_button.grid(row=5, column=1, columnspan=2, pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_simulation)
        self.reset_button.grid(row=6, column=1, columnspan=2, pady=5)

        # Simulation state
        self.running = False

    def update_angle(self, value):
        """Update yaw angle from slider."""
        self.angle = int(value)
        self.angle_value.config(text=f"Current Yaw: {self.angle}°")

    def update_speed(self, value):
        """Update speed from slider (knots to pixels)."""
        self.speed_knots = int(value)
        self.speed_pixels = self.knots_to_pixels(self.speed_knots)  # Convert knots to pixels
        self.speed_value.config(text=f"Current Speed: {self.speed_knots} knots")

    def update_controls(self):
        """Update controls from entry input."""
        try:
            # Update yaw angle from input
            new_angle = float(self.angle_input.get())
            if -180 <= new_angle <= 180:
                self.angle = new_angle
                self.angle_slider.set(new_angle)
                self.angle_value.config(text=f"Current Yaw: {self.angle}°")
            else:
                print("Error: Yaw angle must be between -180 and 180 degrees.")

            # Update speed from input (convert knots to pixels)
            new_speed = float(self.speed_input.get())
            if new_speed >= 0:
                self.speed_knots = new_speed
                self.speed_pixels = self.knots_to_pixels(new_speed)  # Convert knots to pixels
                self.speed_slider.set(new_speed)
                self.speed_value.config(text=f"Current Speed: {self.speed_knots} knots")
            else:
                print("Error: Speed must be non-negative.")
        except ValueError:
            print("Error: Invalid input. Please enter valid numbers.")

    def knots_to_pixels(self, knots):
        """Convert knots to pixels per update (for simplicity, using a conversion factor)."""
        # 1 knot = 0.53996 m/s ≈ 1 pixel per 2 milliseconds
        # Adjust the factor to get a suitable pixel speed for visualization
        pixels_per_knots = 1  # Adjust this value as needed
        return knots * pixels_per_knots

    def start_simulation(self):
        """Start the simulation."""
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.animate()

    def stop_simulation(self):
        """Stop the simulation."""
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def reset_simulation(self):
        """Reset the simulation."""
        self.stop_simulation()
        self.canvas.delete("all")
        self.x, self.y = self.mWidth//2, self.mHeight//2
        self.angle, self.speed_knots = 0, 0
        self.speed_pixels = 0
        self.trail = []
        self.airplane = self.canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill="red")
        self.angle_slider.set(0)
        self.speed_slider.set(0)
        self.angle_value.config(text="Current Yaw: 0°")
        self.speed_value.config(text="Current Speed: 0 knots")
        self.angle_input.delete(0, tk.END)
        self.speed_input.delete(0, tk.END)
        print("Simulation reset.")

    def update_position(self):
        """Update the position of the airplane based on angle and speed."""
        radians = math.radians(self.angle)
        dx = self.speed_pixels * math.cos(radians)
        dy = -self.speed_pixels * math.sin(radians)  # Negative because canvas y-axis increases downward

        self.x += dx
        self.y += dy

        # Handle canvas boundaries (wrap around)
        if self.x < 0: self.x = self.mWidth
        if self.x > self.mWidth: self.x = 0
        if self.y < 0: self.y = self.mHeight
        if self.y > self.mHeight: self.y = 0

        # Update trajectory
        self.trail.append((self.x, self.y))
        if len(self.trail) > 1:
            self.canvas.create_line(self.trail[-2], self.trail[-1], fill="blue")

        # Update airplane's position on canvas
        self.canvas.coords(self.airplane, self.x - 5, self.y - 5, self.x + 5, self.y + 5)

    def animate(self):
        """Animate the airplane's movement."""
        if self.running:
            self.update_position()
            self.root.after(50, self.animate)  # Update every 50 ms


def main():
    root = tk.Tk()
    simulation = AirplaneSimulation(root)
    root.mainloop()


if __name__ == "__main__":
    main()
