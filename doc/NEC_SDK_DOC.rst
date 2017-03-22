Help on module nec_pd_sdk:

NAME
    nec_pd_sdk - nec_pd_sdk.py - High level functions for communicating via LAN or RS232 with NEC large-screen displays.

FILE
    c:\development\python projects\necpdsdk\nec_pd_sdk\nec_pd_sdk.py

DESCRIPTION
    Revision: 170322

CLASSES
    __builtin__.object
        NECPD
    __builtin__.tuple(__builtin__.object)
        PDAutoTileMatrixTuple
        PDDateTimeTuple
        PDDaylightSavingsTuple
        PDHelperProofOfPlayLogItemTuple
        PDOpCodeGetSetTuple
        PDPIPPBPProfileTuple
        PDProofOfPlayLogItemTuple
        PDProofOfPlayStatusTuple
        PDScheduleTuple
        PDTileMatrixProfileTuple
    serial.serialwin32.Serial(serial.serialutil.SerialBase)
        MySerial
    
    class MySerial(serial.serialwin32.Serial)
     |  Add our own functions for serial support to mimic those in 'socket', so we can use the same
     |  function names.
     |  
     |  Method resolution order:
     |      MySerial
     |      serial.serialwin32.Serial
     |      serial.serialutil.SerialBase
     |      io.RawIOBase
     |      _io._RawIOBase
     |      io.IOBase
     |      _io._IOBase
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  recv(self, length)
     |  
     |  sendall(self, data)
     |  
     |  settimeout(self, length)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  __abstractmethods__ = frozenset([])
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from serial.serialwin32.Serial:
     |  
     |  __init__(self, *args, **kwargs)
     |  
     |  cancel_read(self)
     |      Cancel a blocking read operation, may be called from other thread
     |  
     |  cancel_write(self)
     |      Cancel a blocking write operation, may be called from other thread
     |  
     |  close(self)
     |      Close port
     |  
     |  flush(self)
     |      Flush of file like objects. In this case, wait until all data
     |      is written.
     |  
     |  open(self)
     |      Open port with current settings. This may throw a SerialException
     |      if the port cannot be opened.
     |  
     |  read(self, size=1)
     |      Read size bytes from the serial port. If a timeout is set it may
     |      return less characters as requested. With no timeout it will block
     |      until the requested number of bytes is read.
     |  
     |  reset_input_buffer(self)
     |      Clear input buffer, discarding all that is in the buffer.
     |  
     |  reset_output_buffer(self)
     |      Clear output buffer, aborting the current output and discarding all
     |      that is in the buffer.
     |  
     |  set_buffer_size(self, rx_size=4096, tx_size=None)
     |      Recommend a buffer size to the driver (device driver can ignore this
     |      value). Must be called before the port is opened.
     |  
     |  set_output_flow_control(self, enable=True)
     |      Manually control flow - when software flow control is enabled.
     |      This will do the same as if XON (true) or XOFF (false) are received
     |      from the other device and control the transmission accordingly.
     |      WARNING: this function is not portable to different platforms!
     |  
     |  write(self, data)
     |      Output the given byte string over the serial port.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from serial.serialwin32.Serial:
     |  
     |  cd
     |      Read terminal status line: Carrier Detect
     |  
     |  cts
     |      Read terminal status line: Clear To Send
     |  
     |  dsr
     |      Read terminal status line: Data Set Ready
     |  
     |  exclusive
     |      Get the current exclusive access setting.
     |  
     |  in_waiting
     |      Return the number of bytes currently in the input buffer.
     |  
     |  out_waiting
     |      Return how many bytes the in the outgoing buffer
     |  
     |  ri
     |      Read terminal status line: Ring Indicator
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from serial.serialwin32.Serial:
     |  
     |  BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from serial.serialutil.SerialBase:
     |  
     |  __enter__(self)
     |  
     |  __exit__(self, *args, **kwargs)
     |  
     |  __repr__(self)
     |      String representation of the current port settings and its state.
     |  
     |  applySettingsDict(self, d)
     |  
     |  apply_settings(self, d)
     |      Apply stored settings from a dictionary returned from
     |      get_settings(). It's allowed to delete keys from the dictionary. These
     |      values will simply left unchanged.
     |  
     |  flushInput(self)
     |  
     |  flushOutput(self)
     |  
     |  getCD(self)
     |  
     |  getCTS(self)
     |  
     |  getDSR(self)
     |  
     |  getRI(self)
     |  
     |  getSettingsDict(self)
     |  
     |  get_settings(self)
     |      Get current port settings as a dictionary. For use with
     |      apply_settings().
     |  
     |  inWaiting(self)
     |  
     |  iread_until(self, *args, **kwargs)
     |      Read lines, implemented as generator. It will raise StopIteration on
     |      timeout (empty read).
     |  
     |  isOpen(self)
     |  
     |  read_all(self)
     |      Read all bytes currently available in the buffer of the OS.
     |  
     |  read_until(self, terminator='\n', size=None)
     |      Read until a termination sequence is found ('
     |      ' by default), the size
     |              is exceeded or until timeout occurs.
     |  
     |  readable(self)
     |  
     |  readinto(self, b)
     |  
     |  seekable(self)
     |  
     |  sendBreak(self, duration=0.25)
     |  
     |  send_break(self, duration=0.25)
     |      Send break condition. Timed, returns to idle state after given
     |      duration.
     |  
     |  setDTR(self, value=1)
     |  
     |  setPort(self, port)
     |  
     |  setRTS(self, value=1)
     |  
     |  writable(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from serial.serialutil.SerialBase:
     |  
     |  baudrate
     |      Get the current baud rate setting.
     |  
     |  break_condition
     |  
     |  bytesize
     |      Get the current byte size setting.
     |  
     |  dsrdtr
     |      Get the current DSR/DTR flow control setting.
     |  
     |  dtr
     |  
     |  interCharTimeout
     |  
     |  inter_byte_timeout
     |      Get the current inter-character timeout setting.
     |  
     |  parity
     |      Get the current parity setting.
     |  
     |  port
     |      Get the current port setting. The value that was passed on init or using
     |      setPort() is passed back.
     |  
     |  rs485_mode
     |      Enable RS485 mode and apply new settings, set to None to disable.
     |      See serial.rs485.RS485Settings for more info about the value.
     |  
     |  rts
     |  
     |  rtscts
     |      Get the current RTS/CTS flow control setting.
     |  
     |  stopbits
     |      Get the current stop bits setting.
     |  
     |  timeout
     |      Get the current timeout setting.
     |  
     |  writeTimeout
     |  
     |  write_timeout
     |      Get the current timeout setting.
     |  
     |  xonxoff
     |      Get the current XON/XOFF setting.
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from serial.serialutil.SerialBase:
     |  
     |  BYTESIZES = (5, 6, 7, 8)
     |  
     |  PARITIES = ('N', 'E', 'O', 'M', 'S')
     |  
     |  STOPBITS = (1, 1.5, 2)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from _io._RawIOBase:
     |  
     |  readall(...)
     |      Read until EOF, using multiple read() call.
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from io.IOBase:
     |  
     |  __metaclass__ = <class 'abc.ABCMeta'>
     |      Metaclass for defining Abstract Base Classes (ABCs).
     |      
     |      Use this metaclass to create an ABC.  An ABC can be subclassed
     |      directly, and then acts as a mix-in class.  You can also register
     |      unrelated concrete classes (even built-in classes) and unrelated
     |      ABCs as 'virtual subclasses' -- these and their descendants will
     |      be considered subclasses of the registering ABC by the built-in
     |      issubclass() function, but the registering ABC won't show up in
     |      their MRO (Method Resolution Order) nor will method
     |      implementations defined by the registering ABC be callable (not
     |      even via super()).
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from _io._IOBase:
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  fileno(...)
     |      Returns underlying file descriptor if one exists.
     |      
     |      An IOError is raised if the IO object does not use a file descriptor.
     |  
     |  isatty(...)
     |      Return whether this is an 'interactive' stream.
     |      
     |      Return False if it can't be determined.
     |  
     |  next(...)
     |      x.next() -> the next value, or raise StopIteration
     |  
     |  readline(...)
     |      Read and return a line from the stream.
     |      
     |      If limit is specified, at most limit bytes will be read.
     |      
     |      The line terminator is always b'\n' for binary files; for text
     |      files, the newlines argument to open can be used to select the line
     |      terminator(s) recognized.
     |  
     |  readlines(...)
     |      Return a list of lines from the stream.
     |      
     |      hint can be specified to control the number of lines read: no more
     |      lines will be read if the total size (in bytes/characters) of all
     |      lines so far exceeds hint.
     |  
     |  seek(...)
     |      Change stream position.
     |      
     |      Change the stream position to the given byte offset. The offset is
     |      interpreted relative to the position indicated by whence.  Values
     |      for whence are:
     |      
     |      * 0 -- start of stream (the default); offset should be zero or positive
     |      * 1 -- current stream position; offset may be negative
     |      * 2 -- end of stream; offset is usually negative
     |      
     |      Return the new absolute position.
     |  
     |  tell(...)
     |      Return current stream position.
     |  
     |  truncate(...)
     |      Truncate file to size bytes.
     |      
     |      File pointer is left unchanged.  Size defaults to the current IO
     |      position as reported by tell().  Returns the new size.
     |  
     |  writelines(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from _io._IOBase:
     |  
     |  closed
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from _io._IOBase:
     |  
     |  __new__ = <built-in method __new__ of type object>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
    
    class NECPD(__builtin__.object)
     |  Main class for all communications and commands with NEC large-screen displays.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, f)
     |  
     |  close(self)
     |      Closes socket.
     |  
     |  command_asset_data_read = _retry(self, *args, **kwargs)
     |  
     |  command_asset_data_write = _retry(self, *args, **kwargs)
     |  
     |  command_auto_id_complete_notify(self)
     |      Waits for the display to reply after performing Auto ID using command_auto_id_execute
     |      
     |      :return:
     |  
     |  command_auto_id_execute = _retry(self, *args, **kwargs)
     |  
     |  command_auto_id_reset = _retry(self, *args, **kwargs)
     |  
     |  command_auto_power_save_time_read = _retry(self, *args, **kwargs)
     |  
     |  command_auto_power_save_time_write = _retry(self, *args, **kwargs)
     |  
     |  command_auto_standby_time_read = _retry(self, *args, **kwargs)
     |  
     |  command_auto_standby_time_write = _retry(self, *args, **kwargs)
     |  
     |  command_auto_tile_matrix_complete(self)
     |      Waits for the display to reply after performing Auto ID using command_auto_id_execute
     |      
     |      :return:
     |  
     |  command_auto_tile_matrix_execute = _retry(self, *args, **kwargs)
     |  
     |  command_auto_tile_matrix_read = _retry(self, *args, **kwargs)
     |  
     |  command_auto_tile_matrix_reset = _retry(self, *args, **kwargs)
     |  
     |  command_auto_tile_matrix_write = _retry(self, *args, **kwargs)
     |  
     |  command_capabilities_request = _retry(self, *args, **kwargs)
     |  
     |  command_date_and_time_read = _retry(self, *args, **kwargs)
     |  
     |  command_date_and_time_write = _retry(self, *args, **kwargs)
     |  
     |  command_daylight_savings_on_off_read = _retry(self, *args, **kwargs)
     |  
     |  command_daylight_savings_on_off_write = _retry(self, *args, **kwargs)
     |  
     |  command_daylight_savings_read = _retry(self, *args, **kwargs)
     |  
     |  command_daylight_savings_write = _retry(self, *args, **kwargs)
     |  
     |  command_direct_tv_channel_read = _retry(self, *args, **kwargs)
     |  
     |  command_direct_tv_channel_write = _retry(self, *args, **kwargs)
     |  
     |  command_firmware_version_read = _retry(self, *args, **kwargs)
     |  
     |  command_get_parameter = _retry(self, *args, **kwargs)
     |  
     |  command_get_proof_of_play_current = _retry(self, *args, **kwargs)
     |  
     |  command_get_proof_of_play_number_to_number = _retry(self, *args, **kwargs)
     |  
     |  command_get_proof_of_play_status = _retry(self, *args, **kwargs)
     |  
     |  command_get_timing_report = _retry(self, *args, **kwargs)
     |  
     |  command_input_name_of_designated_terminal_read = _retry(self, *args, **kwargs)
     |  
     |  command_input_name_of_designated_terminal_reset = _retry(self, *args, **kwargs)
     |  
     |  command_input_name_of_designated_terminal_write = _retry(self, *args, **kwargs)
     |  
     |  command_input_name_read = _retry(self, *args, **kwargs)
     |  
     |  command_input_name_reset = _retry(self, *args, **kwargs)
     |  
     |  command_input_name_write = _retry(self, *args, **kwargs)
     |  
     |  command_lan_mac_address_read = _retry(self, *args, **kwargs)
     |  
     |  command_model_name_read = _retry(self, *args, **kwargs)
     |  
     |  command_pbp_pip_profile_contents_read = _retry(self, *args, **kwargs)
     |  
     |  command_pbp_pip_profile_contents_write = _retry(self, *args, **kwargs)
     |  
     |  command_pbp_pip_profile_write = _retry(self, *args, **kwargs)
     |  
     |  command_power_save_mode_read = _retry(self, *args, **kwargs)
     |  
     |  command_power_save_mode_write = _retry(self, *args, **kwargs)
     |  
     |  command_power_status_read = _retry(self, *args, **kwargs)
     |  
     |  command_power_status_set = _retry(self, *args, **kwargs)
     |  
     |  command_save_current_settings = _retry(self, *args, **kwargs)
     |  
     |  command_schedule_read = _retry(self, *args, **kwargs)
     |  
     |  command_schedule_write = _retry(self, *args, **kwargs)
     |  
     |  command_security_enable_read = _retry(self, *args, **kwargs)
     |  
     |  command_security_enable_write = _retry(self, *args, **kwargs)
     |  
     |  command_security_lock_control = _retry(self, *args, **kwargs)
     |  
     |  command_self_diagnosis_status_read = _retry(self, *args, **kwargs)
     |  
     |  command_send_ir_remote_control_code = _retry(self, *args, **kwargs)
     |  
     |  command_serial_number_read = _retry(self, *args, **kwargs)
     |  
     |  command_set_parameter = _retry(self, *args, **kwargs)
     |  
     |  command_set_proof_of_play_operation_mode = _retry(self, *args, **kwargs)
     |  
     |  command_tile_matrix_profile_contents_read = _retry(self, *args, **kwargs)
     |  
     |  command_tile_matrix_profile_contents_write = _retry(self, *args, **kwargs)
     |  
     |  command_tile_matrix_profile_write = _retry(self, *args, **kwargs)
     |  
     |  helper_asset_data_read(self)
     |      Helper function that reads the entire asset data string by combining chunks using
     |      "command_asset_data_read".
     |      
     |      :return:
     |  
     |  helper_asset_data_write(self, in_string)
     |      Helper function that writes the asset data string as chunks.
     |      
     |      :param in_string:
     |      :return:
     |  
     |  helper_capabilities_request(self)
     |      Reads the entire capability string from the display.
     |      
     |      :return: the capability string
     |  
     |  helper_date_and_time_read(self)
     |      Performs "command_date_and_time_read" and converts the reply to a Python datetime.
     |      
     |      :return: a datetime of "command_date_and_time_read", daylight_savings
     |  
     |  helper_date_and_time_write(self, in_datetime, in_daylight_savings=0)
     |      Helper function for helper_date_and_time_write that takes a 'datetime'.
     |      
     |      :param in_datetime: a Python datetime
     |      :param in_daylight_savings:
     |      :return: same as command_date_and_time_write
     |  
     |  helper_date_and_time_write_keep_daylight_savings_setting(self, in_datetime)
     |      Helper function for helper_date_and_time_write that takes a 'datetime' but maintains the current
     |      daylight savings on/off setting currently in the display
     |      
     |      :param in_datetime: a Python datetime
     |      :return: same as command_date_and_time_write
     |  
     |  helper_firmware_versions_list(self)
     |      Reads the firmware version(s) from the display. If the display doesn't support
     |      'command_firmware_version_read' then it reads the capability string and parses
     |      it to get the version from the 'mpu_ver()'.
     |      
     |      :return: a list of firmware version strings
     |  
     |  helper_get_fan_statuses(self)
     |      Gets the fan status for all available fans.
     |      
     |      :return: a list of the text status of each available fan
     |  
     |  helper_get_long_power_on_hours(self)
     |      Reads the total power on time in minutes using new 2 x 32 bit opcodes.
     |      Note: Normally use the function "helper_get_power_on_hours" instead of calling this directly
     |      
     |      :return: power on hours as a value
     |  
     |  helper_get_long_total_operating_hours(self)
     |      Reads the total operating time in minutes using new 2 x 32 bit opcodes.
     |      Note: Normally use the function "helper_get_total_operating_hours" instead of calling this directly
     |      
     |      :return: total operating hours as a value
     |  
     |  helper_get_power_on_hours(self)
     |      Reads the total power on hours. First tries to read using the new 64 bit minutes values.
     |      If that fails it reads using the standard 32 bit 0.5 hour value.
     |      
     |      :return: power on hours as a value
     |  
     |  helper_get_proof_of_play_current(self)
     |      Reads the latest proof of play log from the the display and returns the date & time as a Python datetime.
     |      
     |      :return: PDHelperProofOfPlayLogItemTuple
     |  
     |  helper_get_proof_of_play_number(self, number)
     |      Reads a specific proof of play log from the the display and returns the date & time as a Python datetime.
     |      Note: only support reading 1 log at a time.
     |      
     |      :param number: log number to read (1=first)
     |      :return: PDHelperProofOfPlayLogItemTuple
     |  
     |  helper_get_temperature_sensor_values(self)
     |      Gets the temperature values in 'c for all available temperature sensors.
     |      
     |      :return: a list of values in 'c corresponding to each sensor
     |  
     |  helper_get_total_operating_hours(self)
     |      Reads the total operating hours. First tries to read using the new 64 bit minutes values.
     |      If that fails it reads using the standard 32 bit 0.5 hour value.
     |      
     |      :return: total operating hours as a value
     |  
     |  helper_self_diagnosis_status_text(self)
     |      Performs "command_self_diagnosis_status_read" and formats the reply into
     |      a string of the decoded error code(s).
     |      
     |      :return: single string with decoded error codes separated by ';'
     |  
     |  helper_send_ir_remote_control_codes(self, codes)
     |      Helper function that takes a list of IR codes to send.
     |      
     |      :param codes: list of codes
     |      :return:
     |  
     |  helper_set_destination_monitor_id(self, monitor_id)
     |      Helper function to set the Monitor ID.
     |      
     |      :param monitor_id: Can be specified as a number in the range 1-100, or "All", or "A"-"J" for a group
     |      :return:
     |  
     |  helper_set_parameter_as_percentage(self, opcode, percent)
     |      Sets an opcode based control to a value specified as a percentage value
     |      by reading the control to find the maximum then calculating the new value.
     |      Note: This assumes that the control range starts from 0 and is continuous in range.
     |      
     |      :param opcode: opcode to set
     |      :param percent: value to set as a percentage
     |      :return:
     |  
     |  helper_timing_report_text(self)
     |      Performs "command_get_timing_report" and formats into a readable string.
     |      
     |      :return: string with timing information
     |  
     |  reopen(self)
     |      If the connection is socket based, this closes and reopens the socket to try and flush the buffers.
     |  
     |  set_destination_address(self, address)
     |      Sets the destination address (Monitor ID) for all messages.
     |      
     |      :param address: the "raw" value of the destination address (Monitor ID) sent with each command
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  from_com_port(cls, serial_port) from __builtin__.type
     |      Build a NECPD from a serial port.
     |      
     |      :param serial_port: name of port to try and open
     |  
     |  from_ip_address(cls, address, port=7142) from __builtin__.type
     |      Build a NECPD from an ip address and port.
     |      
     |      :param address: IP address to use
     |      :param port: port to use
     |  
     |  open(cls, address) from __builtin__.type
     |      Build a NECPD from an ip address or port. Try and determine if the address
     |      is an IP address or com port and open appropriately.
     |      
     |      :param address: IP address or serial port name to open
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  reply_destination_address = 0
     |  
     |  reply_message_type = 0
    
    class PDAutoTileMatrixTuple(__builtin__.tuple)
     |  PDAutoTileMatrixTuple(h_monitors, v_monitors, pattern_id, current_input_select, tile_matrix_mem)
     |  
     |  Method resolution order:
     |      PDAutoTileMatrixTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDAutoTileMatrixTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDAutoTileMatrixTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, h_monitors, v_monitors, pattern_id, current_input_select, tile_matrix_mem)
     |      Create new instance of PDAutoTileMatrixTuple(h_monitors, v_monitors, pattern_id, current_input_select, tile_matrix_mem)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  current_input_select
     |      Alias for field number 3
     |  
     |  h_monitors
     |      Alias for field number 0
     |  
     |  pattern_id
     |      Alias for field number 2
     |  
     |  tile_matrix_mem
     |      Alias for field number 4
     |  
     |  v_monitors
     |      Alias for field number 1
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('h_monitors', 'v_monitors', 'pattern_id', 'current_input_se...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDDateTimeTuple(__builtin__.tuple)
     |  PDDateTimeTuple(status, year, month, day, weekday, hour, minute, daylight_savings)
     |  
     |  Method resolution order:
     |      PDDateTimeTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDDateTimeTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDDateTimeTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, status, year, month, day, weekday, hour, minute, daylight_savings)
     |      Create new instance of PDDateTimeTuple(status, year, month, day, weekday, hour, minute, daylight_savings)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  day
     |      Alias for field number 3
     |  
     |  daylight_savings
     |      Alias for field number 7
     |  
     |  hour
     |      Alias for field number 5
     |  
     |  minute
     |      Alias for field number 6
     |  
     |  month
     |      Alias for field number 2
     |  
     |  status
     |      Alias for field number 0
     |  
     |  weekday
     |      Alias for field number 4
     |  
     |  year
     |      Alias for field number 1
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('status', 'year', 'month', 'day', 'weekday', 'hour', 'minut...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDDaylightSavingsTuple(__builtin__.tuple)
     |  PDDaylightSavingsTuple(status, begin_month, begin_day1, begin_day2, begin_time_hour, begin_time_minute, end_month, end_day1, end_day2, end_time_hour, end_time_minute, time_difference)
     |  
     |  Method resolution order:
     |      PDDaylightSavingsTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDDaylightSavingsTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDDaylightSavingsTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, status, begin_month, begin_day1, begin_day2, begin_time_hour, begin_time_minute, end_month, end_day1, end_day2, end_time_hour, end_time_minute, time_difference)
     |      Create new instance of PDDaylightSavingsTuple(status, begin_month, begin_day1, begin_day2, begin_time_hour, begin_time_minute, end_month, end_day1, end_day2, end_time_hour, end_time_minute, time_difference)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  begin_day1
     |      Alias for field number 2
     |  
     |  begin_day2
     |      Alias for field number 3
     |  
     |  begin_month
     |      Alias for field number 1
     |  
     |  begin_time_hour
     |      Alias for field number 4
     |  
     |  begin_time_minute
     |      Alias for field number 5
     |  
     |  end_day1
     |      Alias for field number 7
     |  
     |  end_day2
     |      Alias for field number 8
     |  
     |  end_month
     |      Alias for field number 6
     |  
     |  end_time_hour
     |      Alias for field number 9
     |  
     |  end_time_minute
     |      Alias for field number 10
     |  
     |  status
     |      Alias for field number 0
     |  
     |  time_difference
     |      Alias for field number 11
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('status', 'begin_month', 'begin_day1', 'begin_day2', 'begin...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDHelperProofOfPlayLogItemTuple(__builtin__.tuple)
     |  PDHelperProofOfPlayLogItemTuple(status, log_number, input, signal_h_resolution, signal_v_resolution, audio_input, audio_input_status, picture_status, audio_status, date_time, reserved_1, reserved_2, reserved_3)
     |  
     |  Method resolution order:
     |      PDHelperProofOfPlayLogItemTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDHelperProofOfPlayLogItemTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDHelperProofOfPlayLogItemTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, status, log_number, input, signal_h_resolution, signal_v_resolution, audio_input, audio_input_status, picture_status, audio_status, date_time, reserved_1, reserved_2, reserved_3)
     |      Create new instance of PDHelperProofOfPlayLogItemTuple(status, log_number, input, signal_h_resolution, signal_v_resolution, audio_input, audio_input_status, picture_status, audio_status, date_time, reserved_1, reserved_2, reserved_3)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  audio_input
     |      Alias for field number 5
     |  
     |  audio_input_status
     |      Alias for field number 6
     |  
     |  audio_status
     |      Alias for field number 8
     |  
     |  date_time
     |      Alias for field number 9
     |  
     |  input
     |      Alias for field number 2
     |  
     |  log_number
     |      Alias for field number 1
     |  
     |  picture_status
     |      Alias for field number 7
     |  
     |  reserved_1
     |      Alias for field number 10
     |  
     |  reserved_2
     |      Alias for field number 11
     |  
     |  reserved_3
     |      Alias for field number 12
     |  
     |  signal_h_resolution
     |      Alias for field number 3
     |  
     |  signal_v_resolution
     |      Alias for field number 4
     |  
     |  status
     |      Alias for field number 0
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('status', 'log_number', 'input', 'signal_h_resolution', 'si...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDOpCodeGetSetTuple(__builtin__.tuple)
     |  PDOpCodeGetSetTuple(result, opcode, type, max_value, current_value)
     |  
     |  Method resolution order:
     |      PDOpCodeGetSetTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDOpCodeGetSetTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDOpCodeGetSetTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, result, opcode, type, max_value, current_value)
     |      Create new instance of PDOpCodeGetSetTuple(result, opcode, type, max_value, current_value)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  current_value
     |      Alias for field number 4
     |  
     |  max_value
     |      Alias for field number 3
     |  
     |  opcode
     |      Alias for field number 1
     |  
     |  result
     |      Alias for field number 0
     |  
     |  type
     |      Alias for field number 2
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('result', 'opcode', 'type', 'max_value', 'current_value')
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDPIPPBPProfileTuple(__builtin__.tuple)
     |  PDPIPPBPProfileTuple(profile_number, pip_pbp_mode, picture1_input, picture2_input, picture3_input, picture4_input, picture1_size, picture2_size, picture3_size, picture4_size, picture1_aspect, picture2_aspect, picture3_aspect, picture4_aspect, picture1_h_position, picture2_h_position, picture3_h_position, picture4_h_position, picture1_v_position, picture2_v_position, picture3_v_position, picture4_v_position, reserved_11, reserved_12, reserved_13, reserved_14, reserved_15, reserved_16, reserved_17, reserved_18, reserved_19, reserved_20, reserved_21, reserved_22)
     |  
     |  Method resolution order:
     |      PDPIPPBPProfileTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDPIPPBPProfileTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDPIPPBPProfileTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, profile_number, pip_pbp_mode, picture1_input, picture2_input, picture3_input, picture4_input, picture1_size, picture2_size, picture3_size, picture4_size, picture1_aspect, picture2_aspect, picture3_aspect, picture4_aspect, picture1_h_position, picture2_h_position, picture3_h_position, picture4_h_position, picture1_v_position, picture2_v_position, picture3_v_position, picture4_v_position, reserved_11, reserved_12, reserved_13, reserved_14, reserved_15, reserved_16, reserved_17, reserved_18, reserved_19, reserved_20, reserved_21, reserved_22)
     |      Create new instance of PDPIPPBPProfileTuple(profile_number, pip_pbp_mode, picture1_input, picture2_input, picture3_input, picture4_input, picture1_size, picture2_size, picture3_size, picture4_size, picture1_aspect, picture2_aspect, picture3_aspect, picture4_aspect, picture1_h_position, picture2_h_position, picture3_h_position, picture4_h_position, picture1_v_position, picture2_v_position, picture3_v_position, picture4_v_position, reserved_11, reserved_12, reserved_13, reserved_14, reserved_15, reserved_16, reserved_17, reserved_18, reserved_19, reserved_20, reserved_21, reserved_22)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  picture1_aspect
     |      Alias for field number 10
     |  
     |  picture1_h_position
     |      Alias for field number 14
     |  
     |  picture1_input
     |      Alias for field number 2
     |  
     |  picture1_size
     |      Alias for field number 6
     |  
     |  picture1_v_position
     |      Alias for field number 18
     |  
     |  picture2_aspect
     |      Alias for field number 11
     |  
     |  picture2_h_position
     |      Alias for field number 15
     |  
     |  picture2_input
     |      Alias for field number 3
     |  
     |  picture2_size
     |      Alias for field number 7
     |  
     |  picture2_v_position
     |      Alias for field number 19
     |  
     |  picture3_aspect
     |      Alias for field number 12
     |  
     |  picture3_h_position
     |      Alias for field number 16
     |  
     |  picture3_input
     |      Alias for field number 4
     |  
     |  picture3_size
     |      Alias for field number 8
     |  
     |  picture3_v_position
     |      Alias for field number 20
     |  
     |  picture4_aspect
     |      Alias for field number 13
     |  
     |  picture4_h_position
     |      Alias for field number 17
     |  
     |  picture4_input
     |      Alias for field number 5
     |  
     |  picture4_size
     |      Alias for field number 9
     |  
     |  picture4_v_position
     |      Alias for field number 21
     |  
     |  pip_pbp_mode
     |      Alias for field number 1
     |  
     |  profile_number
     |      Alias for field number 0
     |  
     |  reserved_11
     |      Alias for field number 22
     |  
     |  reserved_12
     |      Alias for field number 23
     |  
     |  reserved_13
     |      Alias for field number 24
     |  
     |  reserved_14
     |      Alias for field number 25
     |  
     |  reserved_15
     |      Alias for field number 26
     |  
     |  reserved_16
     |      Alias for field number 27
     |  
     |  reserved_17
     |      Alias for field number 28
     |  
     |  reserved_18
     |      Alias for field number 29
     |  
     |  reserved_19
     |      Alias for field number 30
     |  
     |  reserved_20
     |      Alias for field number 31
     |  
     |  reserved_21
     |      Alias for field number 32
     |  
     |  reserved_22
     |      Alias for field number 33
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('profile_number', 'pip_pbp_mode', 'picture1_input', 'pictur...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDProofOfPlayLogItemTuple(__builtin__.tuple)
     |  PDProofOfPlayLogItemTuple(status, log_number, input, signal_h_resolution, signal_v_resolution, audio_input, audio_input_status, picture_status, audio_status, year, month, day, hour, minute, second, reserved_1, reserved_2, reserved_3)
     |  
     |  Method resolution order:
     |      PDProofOfPlayLogItemTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDProofOfPlayLogItemTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDProofOfPlayLogItemTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, status, log_number, input, signal_h_resolution, signal_v_resolution, audio_input, audio_input_status, picture_status, audio_status, year, month, day, hour, minute, second, reserved_1, reserved_2, reserved_3)
     |      Create new instance of PDProofOfPlayLogItemTuple(status, log_number, input, signal_h_resolution, signal_v_resolution, audio_input, audio_input_status, picture_status, audio_status, year, month, day, hour, minute, second, reserved_1, reserved_2, reserved_3)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  audio_input
     |      Alias for field number 5
     |  
     |  audio_input_status
     |      Alias for field number 6
     |  
     |  audio_status
     |      Alias for field number 8
     |  
     |  day
     |      Alias for field number 11
     |  
     |  hour
     |      Alias for field number 12
     |  
     |  input
     |      Alias for field number 2
     |  
     |  log_number
     |      Alias for field number 1
     |  
     |  minute
     |      Alias for field number 13
     |  
     |  month
     |      Alias for field number 10
     |  
     |  picture_status
     |      Alias for field number 7
     |  
     |  reserved_1
     |      Alias for field number 15
     |  
     |  reserved_2
     |      Alias for field number 16
     |  
     |  reserved_3
     |      Alias for field number 17
     |  
     |  second
     |      Alias for field number 14
     |  
     |  signal_h_resolution
     |      Alias for field number 3
     |  
     |  signal_v_resolution
     |      Alias for field number 4
     |  
     |  status
     |      Alias for field number 0
     |  
     |  year
     |      Alias for field number 9
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('status', 'log_number', 'input', 'signal_h_resolution', 'si...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDProofOfPlayStatusTuple(__builtin__.tuple)
     |  PDProofOfPlayStatusTuple(error_status, total_number, maximum_number, current_status)
     |  
     |  Method resolution order:
     |      PDProofOfPlayStatusTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDProofOfPlayStatusTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDProofOfPlayStatusTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, error_status, total_number, maximum_number, current_status)
     |      Create new instance of PDProofOfPlayStatusTuple(error_status, total_number, maximum_number, current_status)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  current_status
     |      Alias for field number 3
     |  
     |  error_status
     |      Alias for field number 0
     |  
     |  maximum_number
     |      Alias for field number 2
     |  
     |  total_number
     |      Alias for field number 1
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('error_status', 'total_number', 'maximum_number', 'current_...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDScheduleTuple(__builtin__.tuple)
     |  PDScheduleTuple(status, program_no, turn_on_hour, turn_on_minute, turn_off_hour, turn_off_minute, timer_input, week_setting, option, picture_mode, extension_1, extension_2, extension_3, extension_4, extension_5, extension_6, extension_7)
     |  
     |  Method resolution order:
     |      PDScheduleTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDScheduleTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDScheduleTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, status, program_no, turn_on_hour, turn_on_minute, turn_off_hour, turn_off_minute, timer_input, week_setting, option, picture_mode, extension_1, extension_2, extension_3, extension_4, extension_5, extension_6, extension_7)
     |      Create new instance of PDScheduleTuple(status, program_no, turn_on_hour, turn_on_minute, turn_off_hour, turn_off_minute, timer_input, week_setting, option, picture_mode, extension_1, extension_2, extension_3, extension_4, extension_5, extension_6, extension_7)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  extension_1
     |      Alias for field number 10
     |  
     |  extension_2
     |      Alias for field number 11
     |  
     |  extension_3
     |      Alias for field number 12
     |  
     |  extension_4
     |      Alias for field number 13
     |  
     |  extension_5
     |      Alias for field number 14
     |  
     |  extension_6
     |      Alias for field number 15
     |  
     |  extension_7
     |      Alias for field number 16
     |  
     |  option
     |      Alias for field number 8
     |  
     |  picture_mode
     |      Alias for field number 9
     |  
     |  program_no
     |      Alias for field number 1
     |  
     |  status
     |      Alias for field number 0
     |  
     |  timer_input
     |      Alias for field number 6
     |  
     |  turn_off_hour
     |      Alias for field number 4
     |  
     |  turn_off_minute
     |      Alias for field number 5
     |  
     |  turn_on_hour
     |      Alias for field number 2
     |  
     |  turn_on_minute
     |      Alias for field number 3
     |  
     |  week_setting
     |      Alias for field number 7
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('status', 'program_no', 'turn_on_hour', 'turn_on_minute', '...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
    
    class PDTileMatrixProfileTuple(__builtin__.tuple)
     |  PDTileMatrixProfileTuple(profile_number, h_monitors, v_monitors, position, tile_comp)
     |  
     |  Method resolution order:
     |      PDTileMatrixProfileTuple
     |      __builtin__.tuple
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __getstate__(self)
     |      Exclude the OrderedDict from pickling
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  _replace(_self, **kwds)
     |      Return a new PDTileMatrixProfileTuple object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  _make(cls, iterable, new=<built-in method __new__ of type object>, len=<built-in function len>) from __builtin__.type
     |      Make a new PDTileMatrixProfileTuple object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  __new__(_cls, profile_number, h_monitors, v_monitors, position, tile_comp)
     |      Create new instance of PDTileMatrixProfileTuple(profile_number, h_monitors, v_monitors, position, tile_comp)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      Return a new OrderedDict which maps field names to their values
     |  
     |  h_monitors
     |      Alias for field number 1
     |  
     |  position
     |      Alias for field number 3
     |  
     |  profile_number
     |      Alias for field number 0
     |  
     |  tile_comp
     |      Alias for field number 4
     |  
     |  v_monitors
     |      Alias for field number 2
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  _fields = ('profile_number', 'h_monitors', 'v_monitors', 'position', '...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from __builtin__.tuple:
     |  
     |  __add__(...)
     |      x.__add__(y) <==> x+y
     |  
     |  __contains__(...)
     |      x.__contains__(y) <==> y in x
     |  
     |  __eq__(...)
     |      x.__eq__(y) <==> x==y
     |  
     |  __ge__(...)
     |      x.__ge__(y) <==> x>=y
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __gt__(...)
     |      x.__gt__(y) <==> x>y
     |  
     |  __hash__(...)
     |      x.__hash__() <==> hash(x)
     |  
     |  __iter__(...)
     |      x.__iter__() <==> iter(x)
     |  
     |  __le__(...)
     |      x.__le__(y) <==> x<=y
     |  
     |  __len__(...)
     |      x.__len__() <==> len(x)
     |  
     |  __lt__(...)
     |      x.__lt__(y) <==> x<y
     |  
     |  __mul__(...)
     |      x.__mul__(n) <==> x*n
     |  
     |  __ne__(...)
     |      x.__ne__(y) <==> x!=y
     |  
     |  __rmul__(...)
     |      x.__rmul__(n) <==> n*x
     |  
     |  count(...)
     |      T.count(value) -> integer -- return number of occurrences of value
     |  
     |  index(...)
     |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.

FUNCTIONS
    retry(function)
        Attempts to retry a command if there was a protocol error.
        Closes and reopens the port to flush the buffers.

DATA
    DISPLAY_DIAGNOSTIC_ERROR_CODES = {0: 'Normal', 112: 'Standby-power +3....
    DISPLAY_FAN_STATUS = {0: 'Off', 1: 'On', 2: 'Error'}
    OPCODE_ADJUST__ASPECT__ASPECT = 624
    OPCODE_ADJUST__ASPECT__BASE_ZOOM = 718
    OPCODE_ADJUST__ASPECT__EXTENSION_H_ZOOM = 4397
    OPCODE_ADJUST__ASPECT__EXTENSION_V_ZOOM = 4398
    OPCODE_ADJUST__ASPECT__EXTENSION_ZOOM = 4396
    OPCODE_ADJUST__ASPECT__ZOOM = 623
    OPCODE_ADJUST__ASPECT__ZOOM_H_EXPANSION = 620
    OPCODE_ADJUST__ASPECT__ZOOM_H_POSITION = 716
    OPCODE_ADJUST__ASPECT__ZOOM_V_EXPANSION = 621
    OPCODE_ADJUST__ASPECT__ZOOM_V_POSITION = 717
    OPCODE_ADJUST__AUTO_SETUP = 30
    OPCODE_ADJUST__CLOCK = 14
    OPCODE_ADJUST__CLOCK_PHASE = 62
    OPCODE_ADJUST__H_POSITION = 32
    OPCODE_ADJUST__H_RESOLUTION = 592
    OPCODE_ADJUST__INPUT_RESOLUTION = 730
    OPCODE_ADJUST__V_POSITION = 48
    OPCODE_ADJUST__V_RESOLUTION = 593
    OPCODE_AMBIENT_BRIGHTNESS_HIGH = 4148
    OPCODE_AMBIENT_BRIGHTNESS_LOW = 4147
    OPCODE_AUDIO__AUDIO_BALANCE = 147
    OPCODE_AUDIO__AUDIO_BASS = 145
    OPCODE_AUDIO__AUDIO_CHANNEL_MODE = 148
    OPCODE_AUDIO__AUDIO_INPUT = 558
    OPCODE_AUDIO__AUDIO_LINE_OUT = 4225
    OPCODE_AUDIO__AUDIO_TREBLE = 143
    OPCODE_AUDIO__AUDIO_VOLUME = 98
    OPCODE_AUDIO__AUDIO_VOLUME_STEP = 4269
    OPCODE_AUDIO__MTS_AUDIO = 556
    OPCODE_AUDIO__MUTE = 141
    OPCODE_AUDIO__OPTION_SLOT_AUDIO = 4272
    OPCODE_AUDIO__PIP_AUDIO = 4224
    OPCODE_AUDIO__SURROUND_SOUND = 564
    OPCODE_AUTO_ADJUST = 4279
    OPCODE_AUTO_BRIGHTNESS = 557
    OPCODE_AUTO_POWER_SAVE_TIME_SEC_X5 = 4342
    OPCODE_AUTO_STANDBY_TIME_SEC_X5 = 4343
    OPCODE_BNC_MODE = 4222
    OPCODE_BOWLING_MODE = 4335
    OPCODE_BRIGHT_SENSOR_READ_READ_ONLY = 693
    OPCODE_CARBON_FOOTPRINT_G_READ_ONLY = 4112
    OPCODE_CARBON_FOOTPRINT_KG_READ_ONLY = 4113
    OPCODE_CARBON_FOOTPRINT_SAVINGS_NO_RESET_G_READ_ONLY = 4136
    OPCODE_CARBON_FOOTPRINT_SAVINGS_NO_RESET_KG_READ_ONLY = 4137
    OPCODE_CARBON_USAGE_G_READ_ONLY = 4134
    OPCODE_CARBON_USAGE_KG_READ_ONLY = 4135
    OPCODE_CARBON_USAGE_NO_RESET_G_READ_ONLY = 4138
    OPCODE_CARBON_USAGE_NO_RESET_KG_READ_ONLY = 4139
    OPCODE_CLOSED_CAPTION = 4228
    OPCODE_COLOR_SYSTEM = 545
    OPCODE_COMMAND_TRANSFER = 4431
    OPCODE_COMPUTE_MODULE_AUTO_POWER_ON = 4477
    OPCODE_COMPUTE_MODULE_IR_SIGNAL = 4479
    OPCODE_COMPUTE_MODULE_MONITOR_CONTROL = 4480
    OPCODE_COMPUTE_MODULE_POWER_SUPPLY = 4476
    OPCODE_COMPUTE_MODULE_POWER_SUPPLY_OFF_DELAY = 4482
    OPCODE_COMPUTE_MODULE_SHUTDOWN_SIGNAL = 4481
    OPCODE_COMPUTE_MODULE_USB_BOOT_MODE = 4478
    OPCODE_COMPUTE_MODULE_WATCHDOG_TIMER_ENABLE = 4507
    OPCODE_COMPUTE_MODULE_WATCHDOG_TIMER_PERIOD_TIME = 4509
    OPCODE_COMPUTE_MODULE_WATCHDOG_TIMER_RESET = 4510
    OPCODE_COMPUTE_MODULE_WATCHDOG_TIMER_START_UP_TIME = 4508
    OPCODE_CONTROL_CEC = 4470
    OPCODE_CONTROL_CEC_AUDIO_RECEIVER = 4472
    OPCODE_CONTROL_CEC_AUTO_TURN_OFF = 4471
    OPCODE_CONTROL_CEC_SEARCH_DEVICE = 4473
    OPCODE_CONTROL_IR_LOCK_SETTINGS_CHANNEL = 4457
    OPCODE_CONTROL_KEY_LOCK_SETTINGS_CHANNEL = 4464
    OPCODE_CONTROL_KEY_LOCK_SETTINGS_INPUT = 4463
    OPCODE_CONTROL_KEY_LOCK_SETTINGS_MAX_VOLUME = 4462
    OPCODE_CONTROL_KEY_LOCK_SETTINGS_MIN_VOLUME = 4461
    OPCODE_CONTROL_KEY_LOCK_SETTINGS_MODE_SELECT = 4458
    OPCODE_CONTROL_KEY_LOCK_SETTINGS_POWER = 4459
    OPCODE_CONTROL_KEY_LOCK_SETTINGS_VOLUME = 4460
    OPCODE_CONTROL_POWER_INDICATOR_SCHEDULE_INDICATOR = 4465
    OPCODE_CONTROL_USB_USB_EXTERNAL_CONTROL = 4467
    OPCODE_CONTROL_USB_USB_PC_SOURCE = 4468
    OPCODE_CONTROL_USB_USB_POWER = 4469
    OPCODE_CONTROL_USB_USB_TOUCH_POWER = 4466
    OPCODE_CSC_GAIN = 714
    OPCODE_CURRENT_LUMINANCE_READ_ONLY = 692
    OPCODE_CUSTOM_DETECT_PRIORITY_1 = 4142
    OPCODE_CUSTOM_DETECT_PRIORITY_2 = 4143
    OPCODE_CUSTOM_DETECT_PRIORITY_3 = 4144
    OPCODE_CUSTOM_DETECT_PRIORITY_4 = 4145
    OPCODE_CUSTOM_DETECT_PRIORITY_5 = 4146
    OPCODE_DDCI = 4286
    OPCODE_DIGITAL_CLOSED_CAPTION = 4257
    OPCODE_DISABLE_SCHEDULE = 742
    OPCODE_DISPLAYPORT_TERMINAL_SELECT = 4337
    OPCODE_DISPLAYPORT_TERMINAL_TYPE = 4338
    OPCODE_DISPLAY_PORT_BIT_RATE = 4377
    OPCODE_DP_POWER_SETTING = 4483
    OPCODE_DSUB_MODE = 4238
    OPCODE_DUAL_LINK_HDCP_SWITCH = 4484
    OPCODE_DVI_MODE = 719
    OPCODE_EDGE_COMPENSATION__MURA = 4232
    OPCODE_EDGE_COMP_BRIGHTNESS = 4237
    OPCODE_EDGE_COMP_TYPE = 4236
    OPCODE_EDID_SWITCH = 4169
    OPCODE_ENABLE_SCHEDULE = 741
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_GAIN_BLUE = 4256
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_GAIN_GREEN = 4255
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_GAIN_RED = 4254
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_OFFSET_BASE_BLUE = 4250
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_OFFSET_BASE_GREEN = 4249
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_OFFSET_BASE_RED = 4248
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_OFFSET_BLUE = 4253
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_OFFSET_GREEN = 4252
    OPCODE_EXPERT_ANALOG_VIDEO__ADC_OFFSET_RED = 4251
    OPCODE_EXTENDED_POWER_SAVE = 4341
    OPCODE_EXTERNAL_CONTROL__EXTERNAL_CONTROL = 4158
    OPCODE_EXTERNAL_CONTROL__ID_ALL_REPLY = 4229
    OPCODE_FAN__FAN_CONTROL = 637
    OPCODE_FAN__FAN_CONTROL_SENSOR_1_SET_TEMPERATURE = 4320
    OPCODE_FAN__FAN_CONTROL_SENSOR_1_TEMPERATURE_FROM_MAX = 4321
    OPCODE_FAN__FAN_CONTROL_SENSOR_2_SET_TEMPERATURE = 4322
    OPCODE_FAN__FAN_CONTROL_SENSOR_2_TEMPERATURE_FROM_MAX = 4323
    OPCODE_FAN__FAN_CONTROL_SENSOR_3_SET_TEMPERATURE = 4324
    OPCODE_FAN__FAN_CONTROL_SENSOR_3_TEMPERATURE_FROM_MAX = 4325
    OPCODE_FAN__FAN_SELECT = 634
    OPCODE_FAN__FAN_SPEED = 4159
    OPCODE_FAN__FAN_STATUS_READ_ONLY = 635
    OPCODE_GAMMA_PROGRAMMABLE_LUT_SIZE = 761
    OPCODE_GROUP_ID = 4223
    OPCODE_HDMIDVI_SELECT = 4376
    OPCODE_HDMI_SIGNAL = 4160
    OPCODE_HDMI_SW_THROUGH = 4486
    OPCODE_HUMAN_SENSING_HUMAN_SENSOR_STATUS = 4428
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_BACKLIGHT = 4294
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_BACKLIGHT_ONOFF = 4317
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_INPUT = 4304
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_INPUT_ONOFF = 4319
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_MODE = 4213
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_READING = 4214
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_START_TIME = 4216
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_THRESHOLD = 4215
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_VOLUME = 4295
    OPCODE_HUMAN_SENSING__HUMAN_SENSING_VOLUME_ONOFF = 4318
    OPCODE_HUMAN_SENSING__HUMAN_SENSOR_ATTACHMENT_STATUS_READ_ONLY = 4336
    OPCODE_IMAGE_FLIP = 727
    OPCODE_INPUT = 96
    OPCODE_INPUT_ALT = 4358
    OPCODE_INPUT_CHANGE = 4230
    OPCODE_INPUT_CHANGE_SUPER_INPUT_1 = 4302
    OPCODE_INPUT_CHANGE_SUPER_INPUT_2 = 4303
    OPCODE_INPUT_CONFIGURATION__BOTTOM = 4393
    OPCODE_INPUT_CONFIGURATION__BOTTOM_LEFT = 4388
    OPCODE_INPUT_CONFIGURATION__BOTTOM_RIGHT = 4389
    OPCODE_INPUT_CONFIGURATION__LEFT = 4390
    OPCODE_INPUT_CONFIGURATION__PRESET_1_MODE = 4383
    OPCODE_INPUT_CONFIGURATION__PRESET_2_MODE = 4384
    OPCODE_INPUT_CONFIGURATION__PRESET_3_MODE = 4385
    OPCODE_INPUT_CONFIGURATION__RIGHT = 4391
    OPCODE_INPUT_CONFIGURATION__TOP = 4392
    OPCODE_INPUT_CONFIGURATION__TOP_LEFT = 4386
    OPCODE_INPUT_CONFIGURATION__TOP_RIGHT = 4387
    OPCODE_INPUT_DETECT = 576
    OPCODE_INTELLIGENT_WIRELESS_DATA = 4332
    OPCODE_INTERNAL_TOUCH = 4485
    OPCODE_IR_CONTROL = 575
    OPCODE_IR_LOCK_SETTINGS_INPUT = 4313
    OPCODE_IR_LOCK_SETTINGS_MAX_VOLUME = 4312
    OPCODE_IR_LOCK_SETTINGS_MIN_VOLUME = 4311
    OPCODE_IR_LOCK_SETTINGS_MODE_SELECT = 4308
    OPCODE_IR_LOCK_SETTINGS_POWER = 4309
    OPCODE_IR_LOCK_SETTINGS_UNLOCK_SELECT_1 = 4314
    OPCODE_IR_LOCK_SETTINGS_UNLOCK_SELECT_2 = 4315
    OPCODE_IR_LOCK_SETTINGS_UNLOCK_SELECT_3 = 4316
    OPCODE_IR_LOCK_SETTINGS_VOLUME = 4310
    OPCODE_ISF = 4096
    OPCODE_ISF_DATA_COPY = 4098
    OPCODE_ISF_MODE = 4097
    OPCODE_KEY_LOCK = 251
    OPCODE_LAN_POWER = 4307
    OPCODE_LONG_CABLE__COMP_DVI = 752
    OPCODE_LONG_CABLE__COMP_DVI2 = 4378
    OPCODE_LONG_CABLE__COMP_HDMI1 = 4379
    OPCODE_LONG_CABLE__COMP_HDMI2 = 4380
    OPCODE_LONG_CABLE__COMP_HDMI3 = 4381
    OPCODE_LONG_CABLE__COMP_HDMI4 = 4382
    OPCODE_LONG_CABLE__COMP_MANUAL_EQUALIZE = 4157
    OPCODE_LONG_CABLE__COMP_MANUAL_GAIN = 4152
    OPCODE_LONG_CABLE__COMP_MANUAL_OFFSET = 4153
    OPCODE_LONG_CABLE__COMP_MANUAL_PEAK = 4151
    OPCODE_LONG_CABLE__COMP_MANUAL_POLE = 4150
    OPCODE_LONG_CABLE__MANUAL_SYNC_TERMINATE = 737
    OPCODE_MEMO_DISPLAY = 4282
    OPCODE_MONITOR_ID = 574
    OPCODE_MONITOR_TYPE_READ_ONLY = 182
    OPCODE_MOTION_COMPENSATION_120HZ = 4231
    OPCODE_MULTI_INPUT_TERMINAL_SETTINGS_DISPLAYPORT = 4455
    OPCODE_MULTI_INPUT_TERMINAL_SETTINGS_HDMI = 4456
    OPCODE_NOISE_REDUCTION = 550
    OPCODE_OFF_TIMER_HOURS = 555
    OPCODE_OPERATING_TIME_ON_30_MIN_READ_ONLY = 255
    OPCODE_OPERATING_TIME_ON__LOWER___MINUTES___READ_ONLY_ = 4607
    OPCODE_OPERATING_TIME_ON__UPPER___MINUTES___READ_ONLY_ = 4606
    OPCODE_OPS__INTERNAL_PC_AUTO_OFF = 4289
    OPCODE_OPS__INTERNAL_PC_FORCE_QUIT = 4291
    OPCODE_OPS__INTERNAL_PC_OFF_WARNING = 4288
    OPCODE_OPS__INTERNAL_PC_START = 4290
    OPCODE_OPS__OPTION_SLOT_POWER = 4161
    OPCODE_OPTION_LAN_ALERT = 4235
    OPCODE_OSD_CLOSE_OSD = 4439
    OPCODE_OSD_KEY_GUIDE = 4474
    OPCODE_OSD__COMMUNICATIONS_INFORMATION = 4375
    OPCODE_OSD__DISPLAY_ID_ON_OSD = 4245
    OPCODE_OSD__INFORMATION_OSD = 573
    OPCODE_OSD__OSD_FLIP = 4280
    OPCODE_OSD__OSD_H_POSITION = 568
    OPCODE_OSD__OSD_LANGUAGE = 104
    OPCODE_OSD__OSD_OFF = 4233
    OPCODE_OSD__OSD_ROTATION = 577
    OPCODE_OSD__OSD_TRANSPARENCY = 696
    OPCODE_OSD__OSD_TURN_OFF_DELAY = 252
    OPCODE_OSD__OSD_V_POSITION = 569
    OPCODE_PICTURE__ADAPTIVE_CONTRAST = 653
    OPCODE_PICTURE__BLACK_LEVEL = 146
    OPCODE_PICTURE__BRIGHTNESS = 16
    OPCODE_PICTURE__COLOR__6_AXIS_COLOR_BLUE = 159
    OPCODE_PICTURE__COLOR__6_AXIS_COLOR_CYAN = 158
    OPCODE_PICTURE__COLOR__6_AXIS_COLOR_GREEN = 157
    OPCODE_PICTURE__COLOR__6_AXIS_COLOR_MAGENTA = 160
    OPCODE_PICTURE__COLOR__6_AXIS_COLOR_RED = 155
    OPCODE_PICTURE__COLOR__6_AXIS_COLOR_YELLOW = 156
    OPCODE_PICTURE__COLOR__COLOR = 543
    OPCODE_PICTURE__COLOR__COLOR_TEMP = 84
    OPCODE_PICTURE__COLOR__GAIN__BLUE_GAIN = 26
    OPCODE_PICTURE__COLOR__GAIN__GREEN_GAIN = 24
    OPCODE_PICTURE__COLOR__GAIN__RED_GAIN = 22
    OPCODE_PICTURE__COLOR__SATURATION = 138
    OPCODE_PICTURE__COLOR__SELECT_COLOR_PRESET = 20
    OPCODE_PICTURE__COLOR__TINT = 144
    OPCODE_PICTURE__CONTRAST = 18
    OPCODE_PICTURE__FILM_MODE = 547
    OPCODE_PICTURE__GAMMA = 616
    OPCODE_PICTURE__NOISE_REDUCTION = 544
    OPCODE_PICTURE__PICTURE_MODE = 538
    OPCODE_PICTURE__SHARPNESS = 140
    OPCODE_PIP__ACTIVE_FRAME = 4365
    OPCODE_PIP__ACTIVE_WINDOW = 4363
    OPCODE_PIP__INPUT_SELECT_WINDOW_1 = 4366
    OPCODE_PIP__INPUT_SELECT_WINDOW_2 = 4367
    OPCODE_PIP__INPUT_SELECT_WINDOW_3 = 4368
    OPCODE_PIP__INPUT_SELECT_WINDOW_4 = 4369
    OPCODE_PIP__KEEP_PIP_MODE = 4226
    OPCODE_PIP__PBP_TYPE = 4277
    OPCODE_PIP__PIP_ASPECT = 4227
    OPCODE_PIP__PIP_H_POSITION = 628
    OPCODE_PIP__PIP_INPUT_SUB_INPUT = 627
    OPCODE_PIP__PIP_MODE = 626
    OPCODE_PIP__PIP_SIZE = 625
    OPCODE_PIP__PIP_SIZE__VARIABLE = 4281
    OPCODE_PIP__PIP_V_POSITION = 629
    OPCODE_PIP__PIVOT_ALL_WINDOWS = 4374
    OPCODE_PIP__PIVOT_WINDOW_1 = 4370
    OPCODE_PIP__PIVOT_WINDOW_2 = 4371
    OPCODE_PIP__PIVOT_WINDOW_3 = 4372
    OPCODE_PIP__PIVOT_WINDOW_4 = 4373
    OPCODE_PIP__TEXT_TICKER_BLEND = 4107
    OPCODE_PIP__TEXT_TICKER_DETECT = 4108
    OPCODE_PIP__TEXT_TICKER_FADE_IN = 4109
    OPCODE_PIP__TEXT_TICKER_MODE = 4104
    OPCODE_PIP__TEXT_TICKER_POSITION = 4105
    OPCODE_PIP__TEXT_TICKER_SIZE = 4106
    OPCODE_POWER_LED_INDICATOR = 702
    OPCODE_POWER_MODE_READ_ONLY = 214
    OPCODE_POWER_ON_DELAY = 728
    OPCODE_POWER_ON_DELAY_LINK_TO_ID = 4284
    OPCODE_POWER_SAVE = 225
    OPCODE_POWER_SAVE_MESSAGE = 4475
    OPCODE_POWER_SAVE_TIMER = 4306
    OPCODE_READ_TEMPERATURE_SENSOR_READ_ONLY = 633
    OPCODE_RESET__ADVANCED_OPTION_RESET = 740
    OPCODE_RESET__COLOR_RESET = 8
    OPCODE_RESET__FACTORY_RESET = 4
    OPCODE_RESET__GAMMA_PROGRAMMABLE_RESET = 760
    OPCODE_RESET__GEOMETRY_RESET = 6
    OPCODE_RESET__MENU_TREE_RESET = 715
    OPCODE_RESET__SOUND_RESET = 561
    OPCODE_RF_TAG_DESTINATION_ID_READ_ONLY = 4334
    OPCODE_ROOM_AMBIENT_BRIGHTNESS_MAX = 4297
    OPCODE_ROOM_LIGHT_SENSING = 4296
    OPCODE_SCAN_CONVERSION = 549
    OPCODE_SCAN_MODE = 218
    OPCODE_SCAN_MODE_ALT = 739
    OPCODE_SCART_MODE = 670
    OPCODE_SCREEN_MUTE = 4278
    OPCODE_SCREEN_SAVER__SCREEN_SAVER_BRIGHTNESS = 732
    OPCODE_SCREEN_SAVER__SCREEN_SAVER_GAMMA = 731
    OPCODE_SCREEN_SAVER__SCREEN_SAVER_MOTION = 733
    OPCODE_SCREEN_SAVER__SCREEN_SAVER_ZOOM = 4149
    OPCODE_SELECT_TEMPERATURE_SENSOR = 632
    OPCODE_SETTINGS = 176
    OPCODE_SHUTDOWN = 4234
    OPCODE_SIDE_BORDER_COLOR = 735
    OPCODE_SIGNAL_INFORMATION = 746
    OPCODE_SPECTRAVIEW_ENGINE__3D_LUTPROG_GAMMA_SELECT = 4203
    OPCODE_SPECTRAVIEW_ENGINE__BLACK_LEVEL_X10 = 4180
    OPCODE_SPECTRAVIEW_ENGINE__COLOR_VISION_EMULATION = 4187
    OPCODE_SPECTRAVIEW_ENGINE__CUSTOM_GAMMA_VALUE = 744
    OPCODE_SPECTRAVIEW_ENGINE__LUMINANCE_SET = 691
    OPCODE_SPECTRAVIEW_ENGINE__METAMERISM = 4188
    OPCODE_SPECTRAVIEW_ENGINE__PICTURE_MODE = 4176
    OPCODE_SPECTRAVIEW_ENGINE__PRESET = 4177
    OPCODE_SPECTRAVIEW_ENGINE__PRINT_PREVIEW_3D_LUT = 4201
    OPCODE_SPECTRAVIEW_ENGINE__RESET_PICTURE_MODE = 4208
    OPCODE_SPECTRAVIEW_ENGINE__SPECTRAVIEW_ENGINE_MODE = 4423
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_COLORSPACE_BLUE_CIE_X_X1000 = 4185
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_COLORSPACE_BLUE_CIE_Y_X1000 = 4186
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_COLORSPACE_GREEN_CIE_X_X1000 = 4183
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_COLORSPACE_GREEN_CIE_Y_X1000 = 4184
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_COLORSPACE_RED_CIE_X_X1000 = 4181
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_COLORSPACE_RED_CIE_Y_X1000 = 4182
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_COLORSPACE_RESET = 4209
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_WHITE_POINT_CIE_X_X1000 = 4178
    OPCODE_SPECTRAVIEW_ENGINE__TARGET_WHITE_POINT_CIE_Y_X1000 = 4179
    OPCODE_STANDBY_MODE = 666
    OPCODE_STILL_CAPTURE = 630
    OPCODE_TEST_PATTERN__TEST_PATTERN_BLUE_LEVEL = 4156
    OPCODE_TEST_PATTERN__TEST_PATTERN_GREEN_LEVEL = 4155
    OPCODE_TEST_PATTERN__TEST_PATTERN_RED_LEVEL = 4154
    OPCODE_TEST_PATTERN__VT_MODE = 707
    OPCODE_TEXT_TICKER__WINDOW_1 = 4394
    OPCODE_TEXT_TICKER__WINDOW_2 = 4395
    OPCODE_TILE_MATRIX__FRAME_COMP_AUTO_VALUE = 4354
    OPCODE_TILE_MATRIX__FRAME_COMP_MANUAL_VALUE = 4355
    OPCODE_TILE_MATRIX__FRAME_COMP_MODE = 4353
    OPCODE_TILE_MATRIX__TILE_MATRIX_H_MONITORS = 720
    OPCODE_TILE_MATRIX__TILE_MATRIX_MEMORY = 4170
    OPCODE_TILE_MATRIX__TILE_MATRIX_MODE = 723
    OPCODE_TILE_MATRIX__TILE_MATRIX_POSITION = 722
    OPCODE_TILE_MATRIX__TILE_MATRIX_TILE_COMP = 725
    OPCODE_TILE_MATRIX__TILE_MATRIX_V_MONITORS = 721
    OPCODE_TILE_MATRIX__V_SCAN_REVERSE_MANUAL = 4357
    OPCODE_TILE_MATRIX__V_SCAN_REVERSE_MODE = 4356
    OPCODE_TOTAL_OPERATING_TIME_30_MIN_READ_ONLY = 250
    OPCODE_TOTAL_OPERATING_TIME__LOWER___MINUTES___READ_ONLY_ = 4603
    OPCODE_TOTAL_OPERATING_TIME__UPPER___MINUTES___READ_ONLY_ = 4602
    OPCODE_TOUCH_PANEL_PC_SOURCE = 4293
    OPCODE_TOUCH_PANEL_POWER_SUPPLY = 4292
    OPCODE_TV_CHANNEL = 139
    OPCODE_UHD_UPSCALING = 4361
    OPCODE_UNIFORMITY_CORRECTION_LEVEL = 750
    OPCODE_VCP_VERSION_READ_ONLY = 223
    OPCODE_VIDEO_AV_INPUT_POWER_SAVE = 726
    OPCODE_VIDEO_LOOP_OUT_SETTING = 4330
    PD_IR_COMMAND_CODES = {'+': 34, '-': 33, '0': 18, '1': 8, '2': 9, '3':...
    PD_POWER_STATES = {'Error': 0, 'Off': 4, 'On': 1, 'Standby': 2, 'Suspe...
    commandStatusReturnedError = PDCommandStatusReturnedError('Command sta...
    connect_timeout = 2.0
    print_function = _Feature((2, 6, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0)...
    reply_timeout = 7.0
    unexpectedReply = PDUnexpectedReplyError('Unexpected reply received',)
    unicode_literals = _Feature((2, 6, 0, 'alpha', 2), (3, 0, 0, 'alpha', ...