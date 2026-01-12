#!/usr/bin/env python3
"""
Test all instances and export results to Excel.
Runs GA on all 7 instances and collects comprehensive statistics.
"""

import time
import pandas as pd
from datetime import datetime
from main import GeneticAlgorithm, get_instance, list_instances

def test_all_instances(output_file="ga_results.xlsx"):
    """
    Test GA on all instances and export to Excel.
    
    Args:
        output_file: Name of Excel file to create
    """
    print("\n" + "="*80)
    print("COMPREHENSIVE GA TESTING - ALL INSTANCES")
    print("="*80)
    print(f"\nOutput file: {output_file}")
    print("This may take 5-15 minutes depending on instance complexity...\n")
    
    instances = list_instances()
    results = []
    
    for idx, instance_name in enumerate(instances, 1):
        print("="*80)
        print(f"Testing {idx}/{len(instances)}: {instance_name}")
        print("="*80)
        
        try:
            # Load instance
            cargo_items, container = get_instance(instance_name)
            
            print(f"Container: {container.width}×{container.depth}m, {len(cargo_items)} cargo items")
            
            # Run GA
            start_time = time.time()
            ga = GeneticAlgorithm(cargo_items, container)
            solution = ga.run(verbose=False)  # Silent mode for batch testing
            elapsed_time = time.time() - start_time
            
            # Get statistics
            stats = ga.get_statistics()
            
            # Calculate metrics
            initial_fitness = stats['fitness_history'][0]
            final_fitness = stats['best_fitness']
            improvement = initial_fitness - final_fitness
            improvement_pct = (improvement / initial_fitness * 100) if initial_fitness > 0 else 0
            
            # COM analysis
            com_x, com_y = solution.get_center_of_mass()
            safe_x_min = container.width * 0.2
            safe_x_max = container.width * 0.8
            safe_y_min = container.depth * 0.2
            safe_y_max = container.depth * 0.2
            com_in_safe_zone = (safe_x_min <= com_x <= safe_x_max and 
                               safe_y_min <= com_y <= safe_y_max)
            
            # Collect results
            result = {
                'Instance': instance_name,
                'Category': 'Basic' if 'basic' in instance_name else 'Challenging',
                'Container_Width': container.width,
                'Container_Depth': container.depth,
                'Max_Weight': container.max_weight,
                'Num_Cargo': len(cargo_items),
                'Total_Weight': sum(c.weight for c in cargo_items),
                'Initial_Fitness': initial_fitness,
                'Final_Fitness': final_fitness,
                'Improvement': improvement,
                'Improvement_Pct': improvement_pct,
                'Best_Generation': stats['best_generation'],
                'Generations_Run': stats['generations_run'],
                'Time_Seconds': elapsed_time,
                'Solution_Complete': solution.complete,
                'Perfect_Solution': final_fitness == 0.0,
                'COM_X': com_x,
                'COM_Y': com_y,
                'COM_In_Safe_Zone': com_in_safe_zone,
                'Best_Order': str(solution.order),
                'Violations': str(list(solution.violations.keys())) if solution.violations else 'None'
            }
            
            results.append(result)
            
            # Print summary
            status = "✓ PERFECT" if final_fitness == 0 else f"⚠ {final_fitness:.2f}"
            print(f"\nResult: {status}")
            print(f"  Initial: {initial_fitness:.2f} → Final: {final_fitness:.2f}")
            print(f"  Improvement: {improvement:.2f} ({improvement_pct:.1f}%)")
            print(f"  Generations: {stats['best_generation']}/{stats['generations_run']}")
            print(f"  Time: {elapsed_time:.2f}s")
            print(f"  COM: ({com_x:.2f}, {com_y:.2f})")
            
        except Exception as e:
            print(f"\n❌ ERROR on {instance_name}: {e}")
            import traceback
            traceback.print_exc()
            
            # Add error result
            results.append({
                'Instance': instance_name,
                'Error': str(e)
            })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Export to Excel with multiple sheets
    print("\n" + "="*80)
    print("EXPORTING TO EXCEL")
    print("="*80)
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: Full results
        df.to_excel(writer, sheet_name='Full Results', index=False)
        
        # Sheet 2: Summary statistics
        summary = df.groupby('Category').agg({
            'Initial_Fitness': ['mean', 'std', 'min', 'max'],
            'Final_Fitness': ['mean', 'std', 'min', 'max'],
            'Improvement_Pct': ['mean', 'std'],
            'Best_Generation': ['mean', 'std'],
            'Time_Seconds': ['mean', 'sum'],
            'Perfect_Solution': 'sum'
        }).round(2)
        summary.to_excel(writer, sheet_name='Summary Stats')
        
        # Sheet 3: Perfect solutions only
        perfect = df[df['Perfect_Solution'] == True]
        if len(perfect) > 0:
            perfect.to_excel(writer, sheet_name='Perfect Solutions', index=False)
        
        # Sheet 4: Fitness history (if available)
        fitness_histories = []
        for idx, instance_name in enumerate(instances):
            try:
                cargo_items, container = get_instance(instance_name)
                ga = GeneticAlgorithm(cargo_items, container)
                ga.run(verbose=False)
                
                # Pad to same length
                history = ga.fitness_history + [ga.fitness_history[-1]] * (501 - len(ga.fitness_history))
                fitness_histories.append({
                    'Generation': list(range(len(ga.fitness_history))),
                    instance_name: ga.fitness_history
                })
            except:
                pass
    
    print(f"\n✓ Excel file created: {output_file}")
    print("\nSheets created:")
    print("  1. Full Results - All data")
    print("  2. Summary Stats - Grouped by category")
    print("  3. Perfect Solutions - Instances that reached fitness = 0.0")
    
    # Print summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    
    print(f"\n{'Instance':<35} {'Initial':<10} {'Final':<10} {'Gen':<8} {'Time':<8} {'Status'}")
    print("-"*80)
    
    for result in results:
        if 'Error' not in result:
            status = "✓ PERFECT" if result['Perfect_Solution'] else "⚠ Stuck"
            print(f"{result['Instance']:<35} "
                  f"{result['Initial_Fitness']:<10.2f} "
                  f"{result['Final_Fitness']:<10.2f} "
                  f"{result['Best_Generation']:<8} "
                  f"{result['Time_Seconds']:<8.1f} "
                  f"{status}")
    
    # Overall statistics
    print("\n" + "="*80)
    print("OVERALL STATISTICS")
    print("="*80)
    
    perfect_count = sum(1 for r in results if r.get('Perfect_Solution', False))
    total_time = sum(r.get('Time_Seconds', 0) for r in results if 'Time_Seconds' in r)
    avg_improvement = sum(r.get('Improvement_Pct', 0) for r in results if 'Improvement_Pct' in r) / len(results)
    
    print(f"\nPerfect solutions: {perfect_count}/{len(instances)}")
    print(f"Total testing time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"Average improvement: {avg_improvement:.1f}%")
    
    print("\n" + "="*80)
    print(f"✓ TESTING COMPLETE - Results saved to {output_file}")
    print("="*80 + "\n")
    
    return df


if __name__ == "__main__":
    import sys
    
    # Check if pandas is installed
    try:
        import pandas as pd
        import openpyxl
    except ImportError:
        print("\n❌ Required libraries not installed!")
        print("Run: pip install pandas openpyxl")
        sys.exit(1)
    
    # Run tests
    output_file = f"ga_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    print("\nThis will test all 7 instances.")
    print("Estimated time: 5-15 minutes")
    
    proceed = input("\nProceed? (y/n): ").strip().lower()
    
    if proceed == 'y':
        df = test_all_instances(output_file)
        print(f"\n✓ Open {output_file} to view detailed results!")
    else:
        print("\nCancelled.")
