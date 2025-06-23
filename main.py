import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import random

st.set_page_config(
    page_title="pH Lab Simulation",
    layout="wide"
)

st.markdown("""
<style>
.test-tube {
    display: inline-block;
    width: 60px;
    height: 150px;
    border: 3px solid black;
    border-radius: 5px;
    margin: 10px;
    position: relative;
}
.ph-indicator {
    position: absolute;
    top: 50%;
    width: 16px;
    height: 16px;
    background: yellow;
    border: 2px solid black;
    border-radius: 50%;
    transform: translateY(-50%);
}
</style>
""", unsafe_allow_html=True)

class pHLabSimulation:
    def __init__(self):
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.current_ph = 7.0
            st.session_state.current_substance = "Distilled Water"
            st.session_state.experiment_history = []
            st.session_state.current_screen = "menu"
            st.session_state.mixing_animation = False
            st.session_state.heating_animation = False
        
        self.acids = {
            "HCl": {"strength": "strong", "initial_ph": 1.0, "color": "#FF3232"},
            "H2SO4": {"strength": "strong", "initial_ph": 0.5, "color": "#FF3232"},
            "CH3COOH": {"strength": "weak", "initial_ph": 2.9, "color": "#FFA500"},
            "HNO3": {"strength": "strong", "initial_ph": 1.2, "color": "#FF3232"},
            "H3PO4": {"strength": "medium", "initial_ph": 2.1, "color": "#FFA500"}
        }
        
        self.bases = {
            "NaOH": {"strength": "strong", "initial_ph": 13.0, "color": "#3232FF"},
            "KOH": {"strength": "strong", "initial_ph": 13.2, "color": "#3232FF"},
            "NH3": {"strength": "weak", "initial_ph": 11.1, "color": "#ADD8E6"},
            "Ca(OH)2": {"strength": "strong", "initial_ph": 12.4, "color": "#3232FF"},
            "Mg(OH)2": {"strength": "weak", "initial_ph": 10.5, "color": "#ADD8E6"}
        }
    
    def get_substance_color(self, ph_value):
        if ph_value < 3:
            return "#FF0000"
        elif ph_value < 7:
            return "#FFA500"
        elif ph_value == 7:
            return "#90EE90"
        elif ph_value < 11:
            return "#ADD8E6"
        else:
            return "#0000FF"
    
    def draw_test_tube(self, ph_value, substance_name):
        color = self.get_substance_color(ph_value)
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="
                width: 60px; 
                height: 150px; 
                border: 3px solid black; 
                border-radius: 5px; 
                background: {color}; 
                margin: auto;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    bottom: -35px;
                    left: -15px;
                    font-size: 12px;
                    font-weight: bold;
                    width: 90px;
                ">pH: {ph_value:.1f}</div>
            </div>
            <div style="margin-top: 45px; font-size: 12px; width: 120px; margin-left: -30px;">
                {substance_name[:20]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def draw_litmus_paper(self, ph_value):
        if ph_value < 4.5:
            color = "red"
        elif ph_value > 8.3:
            color = "blue"
        else:
            color = "purple"
        
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="
                width: 30px; 
                height: 100px; 
                background: {color}; 
                border: 2px solid black; 
                margin: auto;
            "></div>
            <div style="margin-top: 10px; font-size: 12px;">Litmus</div>
        </div>
        """, unsafe_allow_html=True)
    
    def draw_ph_scale(self, current_ph):
        position = (current_ph / 14) * 100
        st.markdown(f"""
        <div style="position: relative; margin: 20px 0;">
            <div style="
                height: 30px;
                background: linear-gradient(to right, 
                    #FF0000 0%, #FF4500 14.3%, #FFA500 28.6%, 
                    #FFFF00 42.9%, #90EE90 50%, #00FF00 57.1%, 
                    #0000FF 71.4%, #4B0082 85.7%, #8B00FF 100%);
                border: 2px solid black;
                border-radius: 5px;
            "></div>
            <div class="ph-indicator" style="left: {position}%;"></div>
            <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px;">
                <span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span>
                <span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def get_litmus_color_name(self, ph_value):
        if ph_value < 4.5:
            return "red"
        elif ph_value > 8.3:
            return "blue"
        else:
            return "purple"
    
    def get_nature(self, ph_value):
        if ph_value < 7:
            return "acidic"
        elif ph_value > 7:
            return "basic"
        else:
            return "neutral"
    
    def select_substance(self, substance_name):
        if substance_name == 'water':
            st.session_state.current_ph = 7.0
            st.session_state.current_substance = "Distilled Water"
        elif substance_name in self.acids:
            info = self.acids[substance_name]
            st.session_state.current_ph = info['initial_ph'] + random.uniform(-0.1, 0.1)
            st.session_state.current_substance = substance_name
        elif substance_name in self.bases:
            info = self.bases[substance_name]
            st.session_state.current_ph = info['initial_ph'] + random.uniform(-0.1, 0.1)
            st.session_state.current_substance = substance_name
        
        st.session_state.current_ph = max(0, min(14, st.session_state.current_ph))
    
    def perform_litmus_test(self):
        result = {
            "substance": st.session_state.current_substance,
            "ph": st.session_state.current_ph,
            "litmus_colour": self.get_litmus_color_name(st.session_state.current_ph),
            "nature": self.get_nature(st.session_state.current_ph),
            "timestamp": time.strftime("%H:%M:%S")
        }
        st.session_state.experiment_history.append(result)
        return result
    
    def dilute_solution(self):
        dilution_factor = 2.0
        current_ph = st.session_state.current_ph
        
        if current_ph < 7:
            new_ph = current_ph + np.log10(dilution_factor)
            new_ph = min(new_ph, 7.0)
        elif current_ph > 7:
            new_ph = current_ph - np.log10(dilution_factor)
            new_ph = max(new_ph, 7.0)
        else:
            new_ph = 7.0
        
        st.session_state.current_ph = new_ph
        st.session_state.current_substance += " (diluted)"
    
    def mix_with_water(self):
        st.session_state.mixing_animation = True
        new_ph = (st.session_state.current_ph + 7.0) / 2
        st.session_state.current_ph = new_ph
        st.session_state.current_substance = f"Mixture ({st.session_state.current_substance} + water)"
    
    def heat_solution(self):
        st.session_state.heating_animation = True
        ph_change = random.uniform(-0.3, 0.3)
        st.session_state.current_ph += ph_change
        st.session_state.current_ph = max(0, min(14, st.session_state.current_ph))
        st.session_state.current_substance += " (heated)"
    
    def plot_ph_graph(self):
        if not st.session_state.experiment_history:
            st.warning("No experiment data available")
            return
        
        substances = [exp["substance"][:15] + "..." if len(exp["substance"]) > 15 
                     else exp["substance"] for exp in st.session_state.experiment_history]
        ph_values = [exp["ph"] for exp in st.session_state.experiment_history]
        colors = ['red' if ph < 7 else 'blue' if ph > 7 else 'green' for ph in ph_values]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.bar(range(len(substances)), ph_values, color=colors, alpha=0.7)
        
        ax.axhline(y=7, color='black', linestyle='--', alpha=0.5, label='Neutral pH')
        ax.set_xlabel('Experimental Substances')
        ax.set_ylabel('pH Value')
        ax.set_title('pH Graph of Experiments')
        ax.set_xticks(range(len(substances)))
        ax.set_xticklabels(substances, rotation=45, ha='right')
        ax.set_ylim(0, 14)
        ax.grid(True, alpha=0.3)
        
        for i, (bar, ph) in enumerate(zip(bars, ph_values)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   f'{ph:.1f}', ha='center', va='bottom')
        
        ax.axhspan(0, 7, alpha=0.1, color='red', label='Acidic zone')
        ax.axhspan(7, 14, alpha=0.1, color='blue', label='Basic zone')
        
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
    
    def reset_experiment(self):
        st.session_state.experiment_history = []
        st.session_state.current_ph = 7.0
        st.session_state.current_substance = "Distilled Water"
    
    def draw_menu_screen(self):
        st.title("pH LAB SIMULATION")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Controls")
            
            if st.button("Choose Substance", use_container_width=True):
                st.session_state.current_screen = "substance_selection"
                st.rerun()
            
            if st.button("Use Litmus Paper", use_container_width=True):
                st.session_state.current_screen = "litmus_test"
                st.rerun()
            
            if st.button("Drag Drop Tube", use_container_width=True):
                st.session_state.current_screen = "mixing"
                st.rerun()
            
            if st.button("Show pH Graph", use_container_width=True):
                self.plot_ph_graph()
            
            if st.button("View History", use_container_width=True):
                st.session_state.current_screen = "history"
                st.rerun()
            
            if st.button("Reset Experiment", use_container_width=True):
                self.reset_experiment()
                st.rerun()
            
            st.markdown("---")
            st.write(f"**Current Substance:** {st.session_state.current_substance}")
            st.write(f"**Current pH:** {st.session_state.current_ph:.2f}")
            st.write(f"**Experiments:** {len(st.session_state.experiment_history)}")
        
        with col2:
            st.subheader("Lab Equipment")
            
            col2a, col2b = st.columns(2)
            with col2a:
                st.write("**Test Tube**")
                self.draw_test_tube(st.session_state.current_ph, st.session_state.current_substance)
            
            with col2b:
                st.write("**pH Scale**")
                self.draw_ph_scale(st.session_state.current_ph)
    
    def draw_substance_selection_screen(self):
        st.title("CHOOSE CHEMICAL SUBSTANCE")
        
        if st.button("← Back", key="back_substances"):
            st.session_state.current_screen = "menu"
            st.rerun()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("ACIDS")
            for name, info in self.acids.items():
                if st.button(f"{name} (pH ≈ {info['initial_ph']})", 
                           key=f"acid_{name}", use_container_width=True):
                    self.select_substance(name)
                    st.session_state.current_screen = "menu"
                    st.rerun()
        
        with col2:
            st.subheader("BASES")
            for name, info in self.bases.items():
                if st.button(f"{name} (pH ≈ {info['initial_ph']})", 
                           key=f"base_{name}", use_container_width=True):
                    self.select_substance(name)
                    st.session_state.current_screen = "menu"
                    st.rerun()
        
        st.markdown("---")
        if st.button("Distilled Water (pH = 7.0)", key="water", use_container_width=True):
            self.select_substance('water')
            st.session_state.current_screen = "menu"
            st.rerun()
    
    def draw_litmus_test_screen(self):
        st.title("LITMUS PAPER TEST")
        
        if st.button("← Back", key="back_litmus"):
            st.session_state.current_screen = "menu"
            st.rerun()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Test Tube**")
            self.draw_test_tube(st.session_state.current_ph, st.session_state.current_substance)
        
        with col2:
            st.write("**Litmus Paper**")
            self.draw_litmus_paper(st.session_state.current_ph)
        
        with col3:
            st.write("**Information**")
            st.write(f"Substance: {st.session_state.current_substance}")
            st.write(f"pH: {st.session_state.current_ph:.2f}")
            st.write(f"Litmus Colour: {self.get_litmus_color_name(st.session_state.current_ph)}")
            st.write(f"Nature: {self.get_nature(st.session_state.current_ph)}")
        
        st.markdown("---")
        if st.button("Perform Test", type="primary", use_container_width=True):
            result = self.perform_litmus_test()
            st.success(f"Test completed! {result['substance']} is {result['nature']} (pH: {result['ph']:.2f})")
            st.rerun()
        
        if st.session_state.experiment_history:
            last_exp = st.session_state.experiment_history[-1]
            st.info(f"Last test: {last_exp['substance']} - {last_exp['nature']}")
    
    def draw_mixing_screen(self):
        st.title("DRAG DROP TEST TUBE")
        
        if st.button("← Back", key="back_mixing"):
            st.session_state.current_screen = "menu"
            st.rerun()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("**Current Solution**")
            self.draw_test_tube(st.session_state.current_ph, st.session_state.current_substance)
            
            if st.session_state.mixing_animation:
                st.write("Mixing...")
                st.session_state.mixing_animation = False
            
            if st.session_state.heating_animation:
                st.write("Heating...")
                st.session_state.heating_animation = False
        
        with col2:
            st.write("**Operations**")
            
            if st.button("Dilute", use_container_width=True):
                old_ph = st.session_state.current_ph
                self.dilute_solution()
                st.success(f"Solution diluted! New pH: {st.session_state.current_ph:.2f}")
                st.rerun()
            
            if st.button("Mix", use_container_width=True):
                old_ph = st.session_state.current_ph
                self.mix_with_water()
                st.success(f"Mixed with water! New pH: {st.session_state.current_ph:.2f}")
                st.rerun()
            
            if st.button("Heat", use_container_width=True):
                old_ph = st.session_state.current_ph
                self.heat_solution()
                change = st.session_state.current_ph - old_ph
                st.success(f"Solution heated. pH changed by {change:+.2f}")
                st.rerun()
        
        st.write(f"Current: {st.session_state.current_substance[:40]}... pH: {st.session_state.current_ph:.2f}")
    
    def draw_history_screen(self):
        st.title("EXPERIMENT HISTORY")
        
        if st.button("← Back", key="back_history"):
            st.session_state.current_screen = "menu"
            st.rerun()
        
        if not st.session_state.experiment_history:
            st.warning("No experiments yet")
        else:
            df = pd.DataFrame(st.session_state.experiment_history)
            df.index = df.index + 1
            
            st.dataframe(
                df[['timestamp', 'substance', 'ph', 'litmus_colour', 'nature']],
                column_config={
                    'timestamp': 'Time',
                    'substance': 'Substance',
                    'ph': st.column_config.NumberColumn('pH', format="%.2f"),
                    'litmus_colour': 'Litmus Color',
                    'nature': 'Nature'
                },
                use_container_width=True
            )
            
            st.write(f"Total experiments: {len(st.session_state.experiment_history)}")
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ph_lab_history_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    def run(self):
        if st.session_state.current_screen == "menu":
            self.draw_menu_screen()
        elif st.session_state.current_screen == "substance_selection":
            self.draw_substance_selection_screen()
        elif st.session_state.current_screen == "litmus_test":
            self.draw_litmus_test_screen()
        elif st.session_state.current_screen == "mixing":
            self.draw_mixing_screen()
        elif st.session_state.current_screen == "history":
            self.draw_history_screen()

if __name__ == "__main__":
    lab = pHLabSimulation()
    lab.run()