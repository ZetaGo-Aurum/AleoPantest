from aleopantest.modules.utilities import PasswordGenerator
import json

def test_v3_structure():
    print("Testing V3.0 Output Structure...")
    gen = PasswordGenerator()
    result = gen.run(length=12)
    
    print(f"Status: {result.get('execution', {}).get('status')}")
    print(f"V3 Certified: {result.get('summary', {}).get('v3_certified')}")
    print(f"Results type: {type(result.get('results'))}")
    
    # Check for empty arrays
    errors = result.get('errors')
    warnings = result.get('warnings')
    print(f"Errors: {errors}")
    print(f"Warnings: {warnings}")
    
    assert result.get('summary', {}).get('v3_certified') == True
    assert isinstance(result.get('results'), list)
    assert errors is not None and len(errors) > 0
    assert warnings is not None and len(warnings) > 0
    
    print("\nFull JSON Structure:")
    print(json.dumps(result, indent=2))
    print("\n[✓] V3.0 Structure Test Passed!")

if __name__ == "__main__":
    test_v3_structure()
