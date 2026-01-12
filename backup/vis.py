import matplotlib.pyplot as plt
from matplotlib.patches import Circle as PltCircle
from matplotlib.patches import Rectangle as PltRectangle
from main import Solution

class CargoVisualizer:
    """Week 7 compatible visualization"""
    
    def __init__(self, solution: Solution):
        self.solution = solution
        self.container = solution.container
    
    def draw(self, title="Cargo Container Loading", show_com=True, show_safe_zone=True):
        """Draw solution using Week 7 visualization style"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Draw container rectangle
        container_rect = PltRectangle(
            (0, 0), 
            self.container.width, 
            self.container.depth,
            fill=False, 
            edgecolor='#F4BA02', 
            linewidth=3, 
            linestyle='-',
            label='Container boundary'
        )
        ax.add_patch(container_rect)
        
        # Draw safe zone (central 60%)
        if show_safe_zone:
            safe_x = self.container.width * 0.2
            safe_y = self.container.depth * 0.2
            safe_w = self.container.width * 0.6
            safe_h = self.container.depth * 0.6
            
            safe_zone = PltRectangle(
                (safe_x, safe_y),
                safe_w,
                safe_h,
                fill=False,
                edgecolor='#4CAF50',
                linewidth=2,
                linestyle='--',
                alpha=0.7,
                label='Safe zone (60%)'
            )
            ax.add_patch(safe_zone)
        
        # Draw cargo items
        for cargo in self.solution.cargo_items:
            if cargo.placed:
                radius = cargo.diameter / 2.0
                
                # Color based on solution quality
                if self.solution.fitness == 0:
                    edge_color = '#4CAF50'  # Green for perfect
                    fill_color = '#4CAF50'
                else:
                    edge_color = '#99D9DD'  # Blue for searching
                    fill_color = '#99D9DD'
                
                cargo_patch = PltCircle(
                    (cargo.x, cargo.y), 
                    radius,
                    fill=True,
                    facecolor=fill_color,
                    alpha=0.3,
                    edgecolor=edge_color,
                    linewidth=2
                )
                ax.add_patch(cargo_patch)
                
                # Center point
                ax.plot(cargo.x, cargo.y, 'o', color=edge_color, markersize=6)
                
                # Label with ID
                ax.text(cargo.x, cargo.y, f'{cargo.id}', 
                       ha='center', va='center', color='#F7F8F9', 
                       fontsize=11, weight='bold')
                
                # Weight below
                ax.text(cargo.x, cargo.y + radius + 0.3, f'{int(cargo.weight)}kg', 
                       ha='center', va='top', color='#F7F8F9', 
                       fontsize=8, style='italic')
        
        # Draw center of mass
        if show_com and self.solution.complete:
            com_x, com_y = self.solution.get_center_of_mass()
            
            # COM marker with crosshair
            ax.plot(com_x, com_y, 'x', color='#FF0000', 
                   markersize=15, markeredgewidth=3, label='Center of Mass')
            
            # Draw reference lines
            ax.plot([com_x, com_x], [0, com_y], 
                   color='#FF0000', linewidth=1, alpha=0.3, linestyle=':')
            ax.plot([0, com_x], [com_y, com_y], 
                   color='#FF0000', linewidth=1, alpha=0.3, linestyle=':')
        
        # Draw origin marker
        ax.plot(0, 0, 'x', color='#F4BA02', markersize=12, 
               markeredgewidth=3, label='Origin (rear left)')
        
        # Set up axes
        ax.set_aspect('equal')
        margin = max(self.container.width, self.container.depth) * 0.1
        ax.set_xlim(-margin, self.container.width + margin)
        ax.set_ylim(-margin, self.container.depth + margin)
        
        # Week 7 styling
        ax.grid(True, alpha=0.3, color='#F7F8F9')
        ax.set_facecolor('#01364C')
        fig.patch.set_facecolor('#01364C')
        ax.tick_params(colors='#F7F8F9')
        for spine in ax.spines.values():
            spine.set_color('#F7F8F9')
        
        # Title with fitness info
        fitness_text = "PERFECT SOLUTION ✓" if self.solution.fitness == 0 else f"Fitness: {self.solution.fitness:.2f}"
        com_x, com_y = self.solution.get_center_of_mass()
        
        title_text = f"{title}\n{fitness_text} | COM: ({com_x:.2f}, {com_y:.2f})"
        ax.set_title(title_text, color='#F7F8F9', fontsize=14, pad=20, weight='bold')
        
        ax.legend(loc='upper right', facecolor='#01364C', edgecolor='#F7F8F9', 
                 labelcolor='#F7F8F9', framealpha=0.9, fontsize=9)
        
        ax.set_xlabel('Width (m)', color='#F7F8F9', fontsize=10)
        ax.set_ylabel('Depth (m)', color='#F7F8F9', fontsize=10)
        
        plt.tight_layout()
        return fig, ax