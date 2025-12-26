# Aleocrophic Interactive CLI System - Implementation Guide

## Overview

This document describes the comprehensive improvements made to the Aleocrophic penetration testing framework to provide an interactive CLI system for beginners while maintaining professional functionality.

## What's Been Improved

### 1. **Parameter Mapping & Flexible Input**

The new `ParameterMapper` class allows tools to accept multiple parameter names for the same value. This means:

- `--ip` and `--host` are interchangeable for IP geolocation
- Users don't need to memorize exact parameter names
- Parameters are automatically normalized

**Example:**
```bash
# Both work the same way:
Aleocrophic run ip-geo --ip 8.8.8.8
Aleocrophic run ip-geo --host 8.8.8.8
```

### 2. **Fixed IP Geolocation Tool**

**Previous Issue:** The tool expected `ip` parameter but CLI was passing `host`

**Solution:**
- Added support for both `ip` and `host` parameters
- Added parameter alias mapping
- Improved validation with clear error messages
- Better API error handling
- More comprehensive location data extraction

**Example:**
```bash
Aleocrophic run ip-geo --ip 8.8.8.8
Aleocrophic run ip-geo --host 1.1.1.1
```

### 3. **Enhanced DDoS Simulator**

**Improvements:**
- Added preset configurations (light, medium, heavy)
- Better parameter validation with safety limits
- Comprehensive legal warnings and disclaimers
- Improved documentation with examples
- Added `--authorized` flag requirement for legal compliance
- Better error handling and user guidance

**Example:**
```bash
# Using presets (safe configurations)
Aleocrophic run ddos-sim --target example.com --type http --preset light --authorized

# Custom configuration
Aleocrophic run ddos-sim --target example.com --type http --duration 30 --threads 10 --authorized
```

### 4. **Interactive Help System**

The CLI now displays comprehensive help for each tool:

```
================================================================================
🛠️  IP Geolocation (v1.1.0)
================================================================================

📝 Description:
IP geolocation untuk mendapatkan lokasi geografis dari IP address...

📚 Usage:
Examples:
  geo = IPGeolocation(); geo.run(ip='8.8.8.8')
  geo = IPGeolocation(); geo.run(host='1.1.1.1')
  
CLI Usage:
  Aleocrophic run ip-geo --ip 8.8.8.8
  Aleocrophic run ip-geo --host 1.1.1.1

🏷️  Tags: osint, geolocation, ip, reconnaissance, location-lookup
📦 Requirements: requests

================================================================================
```

### 5. **New Utility Modules**

#### `interactive_handler.py`
Provides interactive CLI functionality:
- `ParameterMapper`: Maps parameter aliases
- `InteractivePrompt`: Interactive parameter input
- `SafeParameterHandler`: Parameter validation
- `InteractiveCliBuilder`: Build interactive flows

#### `tool_helper.py`
Provides tool parameter utilities:
- `ToolParameterValidator`: Validate all parameter types
- `ToolParameterHelper`: Manage required parameters and hints
- `ToolOutputFormatter`: Format and export results

### 6. **Enhanced BaseTool**

Added `add_warning()` method to support warning messages alongside errors.

## Key Features

### Parameter Validation
Automatic validation for:
- IP addresses (4-octet format, range 0-255)
- URLs (must start with http:// or https://)
- Domain names (valid characters, proper format)
- Port numbers (1-65535)
- Duration and thread counts with safety limits

### Safety Features

1. **DDoS Simulator Safety**
   - Maximum 2-minute duration
   - Maximum 50 concurrent connections
   - Authorization flag required
   - Rate limiting protection
   - Comprehensive legal warnings

2. **Parameter Normalization**
   - Flexible parameter naming
   - Automatic alias resolution
   - Consistent error messages

3. **Validation**
   - Pre-execution validation
   - Clear error messages
   - Helpful hints for correction

### User-Friendly Output

- **Rich formatting** with colors and icons
- **Detailed tool information** before execution
- **Clear error messages** with suggestions
- **Export capability** to JSON or TXT
- **Progress indication** and status messages

## Usage Examples

### IP Geolocation

```bash
# Basic usage
Aleocrophic run ip-geo --ip 8.8.8.8

# Using alias
Aleocrophic run ip-geo --host 1.1.1.1

# View help
Aleocrophic help-tool ip-geo
```

### DDoS Simulator (Authorized Testing Only)

```bash
# Light testing (10 seconds, 5 threads)
Aleocrophic run ddos-sim --target example.com --type http --preset light --authorized

# Medium testing (30 seconds, 10 threads)
Aleocrophic run ddos-sim --target example.com --type http --preset medium --authorized

# Custom configuration
Aleocrophic run ddos-sim --target example.com --type dns --duration 60 --threads 20 --authorized
```

### DNS Lookup

```bash
Aleocrophic run dns --domain google.com
Aleocrophic run dns --domain example.org
```

### Web Phishing

```bash
Aleocrophic run web-phishing --url http://example.com
Aleocrophic run web-phishing --url https://suspicious-site.com
```

## File Structure

### Modified Files

1. **core/base_tool.py**
   - Added `add_warning()` method
   - Added `warnings` list initialization
   - Updated `clear_results()` to clear warnings

2. **core/interactive_handler.py** (NEW)
   - Parameter mapping and aliasing
   - Interactive CLI prompts
   - Parameter validation
   - Help system builders

3. **core/tool_helper.py** (NEW)
   - Parameter validators
   - Parameter helpers
   - Output formatters

4. **modules/osint/ip_geolocation.py**
   - Support for `host` as alias for `ip`
   - Better error handling
   - More complete API field extraction
   - Improved documentation

5. **modules/network/ddos_simulator.py**
   - Preset configurations
   - Better validation
   - Improved documentation
   - Legal warnings
   - Support for `preset` parameter

6. **cli.py**
   - Added `--ip` option alongside `--host`
   - Added `--preset` option for DDoS
   - Added `--authorized` flag
   - Added `--interactive` mode
   - Parameter normalization using `ParameterMapper`
   - Better help display with warnings
   - Improved error reporting

## Implementation Details

### Parameter Mapping

```python
# Define parameter aliases
PARAMETER_ALIASES = {
    'ip': ['host', 'address', 'target_ip'],
    'domain': ['target_domain', 'site'],
    'url': ['target_url', 'website'],
    # ... more mappings
}

# Use it
normalized = ParameterMapper.normalize_params({
    'host': '8.8.8.8',
    'url': 'http://example.com'
})
# Result: {'ip': '8.8.8.8', 'url': 'http://example.com'}
```

### Validation Example

```python
validator = ToolParameterValidator()
is_valid, error = validator.validate_ip('8.8.8.8')
if not is_valid:
    print(f"Error: {error}")
```

## Testing

To test the improvements:

```bash
# Test IP Geolocation with both parameter names
python -m aleo_pantest.cli run ip-geo --ip 8.8.8.8
python -m aleo_pantest.cli run ip-geo --host 1.1.1.1

# Test DDoS Simulator (AUTHORIZED TESTING ONLY)
python -m aleo_pantest.cli run ddos-sim --target example.com --type http --preset light --authorized

# Test DNS
python -m aleo_pantest.cli run dns --domain google.com

# View tool help
python -m aleo_pantest.cli help-tool ip-geo
```

## Security Considerations

### Legal Compliance

1. **DDoS Simulator** explicitly requires `--authorized` flag
2. Legal disclaimers displayed before tool execution
3. Risk levels clearly marked (LOW, MEDIUM, HIGH, CRITICAL)
4. Safety limits enforced in code

### Parameter Validation

1. All inputs validated before execution
2. Clear error messages guide users
3. Type checking for numeric parameters
4. Format validation for IPs, URLs, domains

## Future Enhancements

Potential improvements for future versions:

1. **Interactive Mode** - Full interactive prompts for all tools
2. **Configuration Files** - Save/load parameter presets
3. **Batch Operations** - Run multiple tools in sequence
4. **Advanced Logging** - Detailed execution logs
5. **Report Generation** - Automated PDF/HTML reports
6. **Authentication** - API authentication support
7. **Scheduling** - Schedule tools to run at specific times
8. **Custom Validators** - Per-tool custom validation rules

## Troubleshooting

### IP Geolocation Not Working

**Problem:** "IP address is required"
**Solution:** Use either `--ip` or `--host` parameter
```bash
Aleocrophic run ip-geo --ip 8.8.8.8
```

### DDoS Simulator Rejected

**Problem:** "Requires --authorized flag"
**Solution:** Add `--authorized` flag for legal compliance
```bash
Aleocrophic run ddos-sim --target example.com --type http --preset light --authorized
```

### Invalid Parameter Error

**Problem:** Parameter not recognized
**Solution:** Check documentation or help for that tool
```bash
Aleocrophic help-tool <tool-id>
```

## Development Guidelines

When creating new tools, follow these patterns:

1. **Use ParameterMapper** for flexible parameter names
2. **Implement validate_input()** with comprehensive checks
3. **Add use_warning()** for non-fatal issues
4. **Provide clear error messages** with suggestions
5. **Include comprehensive usage examples** in metadata
6. **Add legal disclaimers** for sensitive tools
7. **Document all parameters** in usage string

## Conclusion

These improvements make Aleocrophic more user-friendly for beginners while maintaining professional functionality for advanced users. The system provides:

- ✅ Flexible parameter naming
- ✅ Comprehensive validation
- ✅ Clear error messages
- ✅ Safety features and legal compliance
- ✅ Rich interactive help
- ✅ Professional output formatting

The framework is now production-ready and suitable for both educational and professional penetration testing scenarios.
