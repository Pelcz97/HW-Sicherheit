TOPLEVEL = top_level
VERILOG_FILES = ${shell ls *.v}
PCF = LatticeiCE40HX8K.pcf
DEVICE = hx8k
YOSYS=yosys
NEXTPNR=nextpnr-ice40
MHZ=12

all: $(TOPLEVEL).rpt $(TOPLEVEL).bin

synth: $(TOPLEVEL).json

pnr: $(TOPLEVEL).asc

$(TOPLEVEL).json: $(VERILOG_FILES)
	$(YOSYS) -Q -T \
	-p "hierarchy -top ${TOPLEVEL}" \
	-p "synth_ice40 ${YOSYS_OPTIONS} -json ${TOPLEVEL}.json" \
	$(VERILOG_FILES)
%.asc: %.json $(PCF)
	$(NEXTPNR) --$(DEVICE) --freq $(MHZ) --json $< --pcf $(PCF) --pcf-allow-unconstrained --asc $@

# does not work as expected yet:
gui: $(TOPLEVEL).json $(PCF) $(TOPLEVEL).asc
	$(NEXTPNR) --$(DEVICE) --json $(TOPLEVEL).json --pcf $(PCF) --asc $(TOPLEVEL).asc --pcf-allow-unconstrained --gui

%.bin: %.asc
	icepack $< $@

%.rpt: %.asc
	icetime -d $(DEVICE) -mtr $@ $<

prog: $(TOPLEVEL).bin
	iceprog -S $<

prog-flash: $(TOPLEVEL).bin
	iceprog $<

sudo-prog: $(TOPLEVEL).bin
	@echo 'Executing prog as root!!!'
	sudo iceprog -S $<

sudo-prog-flash: $(TOPLEVEL).bin
	@echo 'Executing prog as root!!!'
	sudo iceprog $<

clean:
	rm -f $(TOPLEVEL).blif $(TOPLEVEL).asc $(TOPLEVEL).rpt $(TOPLEVEL).bin $(TOPLEVEL).json

.SECONDARY:
.PHONY: all prog clean
